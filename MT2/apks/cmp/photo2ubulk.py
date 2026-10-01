#!/usr/bin/env python3
"""Put your own photo into an ETC2 RGBA .ubulk (same file size as original).

Install once (Termux):
  pkg install python python-numpy python-pillow

Usage:
  python3 photo2ubulk.py photo.jpg
  python3 photo2ubulk.py photo.jpg --width 1024
  python3 photo2ubulk.py photo.jpg --flipy
  python3 photo2ubulk.py photo.jpg -f OtherTexture.ubulk
  python3 photo2ubulk.py --restore

The original is saved once as <file>.bak and is never overwritten.
The photo is stretched to width x height (default 1024 x 1024).
Assumes the file is a chain of mip levels, largest first (normal for UE).
"""
import argparse
import os
import shutil
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("Need numpy and Pillow. In Termux run:\n"
             "  pkg install python python-numpy python-pillow")

# ETC1/ETC2 intensity modifier tables, indexed by (msb << 1) | lsb
MODS = np.array([
    [2, 8, -2, -8], [5, 17, -5, -17], [9, 29, -9, -29], [13, 42, -13, -42],
    [18, 60, -18, -60], [24, 80, -24, -80], [33, 106, -33, -106],
    [47, 183, -47, -183]], dtype=np.float32)

# EAC alpha block: base 253, multiplier 1, table 0, all indices 4 (+2) -> alpha 255
ALPHA = bytes([253, 0x10]) + int("100" * 16, 2).to_bytes(6, "big")

# bit position of pixel (y, x) inside the block index words
POS = np.array([[x * 4 + y for x in range(4)] for y in range(4)], dtype=np.uint32)


def split(arr, flip):
    n = arr.shape[0]
    if flip == 0:
        a, b = arr[:, :, 0:2], arr[:, :, 2:4]
    else:
        a, b = arr[:, 0:2, :], arr[:, 2:4, :]
    return a.reshape(n, 8, -1), b.reshape(n, 8, -1)


def pos_split(flip):
    if flip == 0:
        return POS[:, 0:2].reshape(8), POS[:, 2:4].reshape(8)
    return POS[0:2, :].reshape(8), POS[2:4, :].reshape(8)


def encode_flip(pix, flip):
    """Encode (N,4,4,3) float blocks as ETC1 'individual' mode. Returns (error, 8-byte colors)."""
    n = pix.shape[0]
    a, b = split(pix, flip)
    P = np.stack([a, b], axis=1)                                   # (N,2,8,3)
    base4 = np.clip(np.rint(P.mean(axis=2) / 17.0), 0, 15)         # (N,2,3)
    base8 = base4 * 17.0
    cand = base8[:, :, None, None, None, :] + MODS[None, None, :, None, :, None]
    cand = np.clip(cand, 0, 255)                                   # (N,2,8,1,4,3)
    diff = P[:, :, None, :, None, :] - cand                        # (N,2,8,8,4,3)
    err = (diff * diff).sum(axis=-1)                               # (N,2,8,8,4)
    best_mod = err.argmin(axis=4)                                  # (N,2,8,8)
    tab_err = err.min(axis=4).sum(axis=3)                          # (N,2,8)
    tab = tab_err.argmin(axis=2)                                   # (N,2)
    total = np.take_along_axis(tab_err, tab[:, :, None], axis=2)[:, :, 0].sum(axis=1)

    ni = np.arange(n)[:, None]
    si = np.arange(2)[None, :]
    idx = best_mod[ni, si, tab]                                    # (N,2,8)

    pa, pb = pos_split(flip)
    pos = np.stack([pa, pb])                                       # (2,8)
    msb = np.zeros(n, np.uint32)
    lsb = np.zeros(n, np.uint32)
    for s in range(2):
        for j in range(8):
            v = idx[:, s, j].astype(np.uint32)
            sh = pos[s, j]
            msb |= ((v >> 1) & 1) << sh
            lsb |= (v & 1) << sh

    bi = base4.astype(np.uint8)
    out = np.zeros((n, 8), np.uint8)
    out[:, 0] = (bi[:, 0, 0] << 4) | bi[:, 1, 0]
    out[:, 1] = (bi[:, 0, 1] << 4) | bi[:, 1, 1]
    out[:, 2] = (bi[:, 0, 2] << 4) | bi[:, 1, 2]
    out[:, 3] = (tab[:, 0].astype(np.uint8) << 5) | (tab[:, 1].astype(np.uint8) << 2) | flip
    out[:, 4] = (msb >> 8) & 255
    out[:, 5] = msb & 255
    out[:, 6] = (lsb >> 8) & 255
    out[:, 7] = lsb & 255
    return total, out


def encode_image(rgb):
    """rgb: uint8 (H,W,3), H and W multiples of 4. Returns ETC2 RGBA bytes."""
    h, w = rgb.shape[:2]
    bh, bw = h // 4, w // 4
    blocks = (rgb.reshape(bh, 4, bw, 4, 3).transpose(0, 2, 1, 3, 4)
              .reshape(-1, 4, 4, 3).astype(np.float32))
    res = bytearray()
    step = 4096
    alpha = np.frombuffer(ALPHA, np.uint8)
    for i in range(0, len(blocks), step):
        c = blocks[i:i + step]
        e0, o0 = encode_flip(c, 0)
        e1, o1 = encode_flip(c, 1)
        o = np.where((e1 < e0)[:, None], o1, o0)
        buf = np.empty((len(c), 16), np.uint8)
        buf[:, :8] = alpha
        buf[:, 8:] = o
        res += buf.tobytes()
    return bytes(res)


def level_bytes(w, h):
    return max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * 16


def prepare(img, w, h):
    arr = np.asarray(img.resize((w, h), Image.LANCZOS), dtype=np.uint8)
    ph, pw = (-h) % 4, (-w) % 4
    if ph or pw:
        arr = np.pad(arr, ((0, ph), (0, pw), (0, 0)), mode="edge")
    return arr


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?", help="your photo (jpg/png)")
    ap.add_argument("-f", "--file", default="DesertHDRI.ubulk")
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--height", type=int, default=0)
    ap.add_argument("--flipy", action="store_true", help="flip the photo upside down")
    ap.add_argument("--restore", action="store_true")
    a = ap.parse_args()

    target, backup = a.file, a.file + ".bak"

    if a.restore:
        if not os.path.exists(backup):
            sys.exit(f"No backup found: {backup}")
        shutil.copyfile(backup, target)
        print(f"Restored {target}")
        return

    if not a.image:
        ap.print_help()
        sys.exit(1)
    if not os.path.exists(a.image):
        sys.exit(f"Photo not found: {a.image}")
    if not os.path.exists(target) and not os.path.exists(backup):
        sys.exit(f"File not found: {target} (run in its folder)")
    if not os.path.exists(backup):
        shutil.copyfile(target, backup)
        print(f"Backup saved: {backup}")

    size = os.path.getsize(backup)
    if size % 16:
        sys.exit(f"Size {size} is not a multiple of 16; not plain ETC2 RGBA data.")

    img = Image.open(a.image).convert("RGB")
    if a.flipy:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    w, h = a.width, a.height or a.width
    levels, total = [], 0
    while total + level_bytes(w, h) <= size:
        levels.append((w, h))
        total += level_bytes(w, h)
        if w == 1 and h == 1:
            break
        w, h = max(1, w // 2), max(1, h // 2)
    if not levels:
        sys.exit("Width/height too large for this file.")

    out = bytearray()
    for n, (lw, lh) in enumerate(levels, 1):
        print(f"Level {n}/{len(levels)}: {lw}x{lh} ...", flush=True)
        out += encode_image(prepare(img, lw, lh))

    leftover = size - len(out)
    if leftover:
        avg = np.asarray(img.resize((4, 4), Image.BOX), dtype=np.uint8)
        out += encode_image(avg) * (leftover // 16)

    with open(target, "wb") as f:
        f.write(out)

    print(f"OK: {target}, {len(out)} bytes, {len(levels)} mip levels")
    if leftover:
        print(f"Note: {leftover} bytes did not fit a standard mip chain "
              f"(filled with the photo's average color).")
        print("If the picture looks wrong in the game, try --width 2048 or --width 512.")


if __name__ == "__main__":
    main()
