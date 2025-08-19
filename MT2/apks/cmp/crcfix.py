# -*- coding: utf-8 -*-
# Created By  : Krypton
# Created Date: 8-MAY-24
# version ='1.0'

import zipfile
import sys
import re
import subprocess
from pathlib import Path

YELLOW = "\033[1;33m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
END = "\033[0m"


def patch_crc(file, orig, tofix):
    with open(file, "rb") as f:
        out = f.read()

    repl = out.replace(tofix, orig)

    with open(file + "crc.apk", "wb") as ff:
        ff.write(repl)


def get_crc(file):
    res = []
    with zipfile.ZipFile(file, "r") as f:
        for i in f.infolist():
            if ".dex" in i.filename or "AndroidManifest.xml" in i.filename:
                res.append({"name": i.filename, "crc": i.CRC})
    return res


def le_hex(bytearr):
    return "".join("%02x" % b for b in bytearr)


def check_necessary():
    try:
        subprocess.call(
            ["apksigner", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.call(
            ["keytool"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    except FileNotFoundError as e:
        exit(f"[-] apksigner/keytool not found can't sign")


def create_keystore():
    subprocess.call(
        [
            'keytool -genkey -v -keystore debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US" -sigalg SHA1withRSA'
        ],
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def sign_apk(file):
    if not Path("debug.keystore").is_file():
        create_keystore()
    subprocess.call(
        [
            f"apksigner",
            "sign",
            "--ks",
            "debug.keystore",
            "--key-pass",
            "pass:android",
            "--ks-pass",
            "pass:android",
            "--in",
            file,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        exit(f"{RED}[-] Usage: python {sys.argv[0]} original_apk apk_to_fix{END}")
    check_necessary()

    original = sys.argv[1]
    tofix = sys.argv[2]

    original_crc = get_crc(original)
    tofix_crc = get_crc(tofix)

    for i, j in zip(original_crc, tofix_crc):
        if i["crc"] != j["crc"]:
            print(f"{GREEN}[+] CRC of {i['name']} doesn't match, patching{END}")
            orig_crc_le = i["crc"].to_bytes(4, byteorder="little")
            tofix_crc_le = j["crc"].to_bytes(4, byteorder="little")

            print(f"{YELLOW}[*] Original crc : {le_hex(orig_crc_le)}{END}")
            print(f"{YELLOW}[*] Modified crc : {le_hex(tofix_crc_le)}{END}")
            patch_crc(tofix, orig_crc_le, tofix_crc_le)

    print(f"{GREEN}[+] Signing File{END}")
    sign_apk(tofix + "crc.apk")
    print(f"{GREEN}[+] Done{END}")
