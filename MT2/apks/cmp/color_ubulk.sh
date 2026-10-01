#!/usr/bin/env bash
# Fill an ETC2 RGBA .ubulk file with one solid color (same size as original).
#
# Usage:
#   bash color.sh day
#   bash color.sh 200 50 120
#   bash color.sh "#ff8800"
#   bash color.sh night -f OtherTexture.ubulk
#   bash color.sh --restore
#   bash color.sh --list
#
# The original is saved once as <file>.bak and is never overwritten.

FILE="DesertHDRI.ubulk"

declare -A PRESETS=(
  [day]="135 206 235"   [sunset]="255 140 60"  [night]="15 20 50"
  [dawn]="255 190 150"  [white]="248 248 248"  [gray]="128 128 128"
  [red]="220 30 30"     [green]="60 180 70"    [blue]="30 80 220"
  [yellow]="240 220 60" [purple]="140 60 190"  [black]="0 0 0"
)

die() { echo "$*" >&2; exit 1; }

ARGS=()
RESTORE=0
while [ $# -gt 0 ]; do
  case "$1" in
    -f|--file) FILE="$2"; shift 2 ;;
    --restore) RESTORE=1; shift ;;
    --list)
      for k in "${!PRESETS[@]}"; do echo "$k: ${PRESETS[$k]}"; done | sort
      exit 0 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

BAK="$FILE.bak"

if [ "$RESTORE" = 1 ]; then
  [ -f "$BAK" ] || die "No backup found: $BAK"
  cp "$BAK" "$FILE" && echo "Restored $FILE from $BAK"
  exit 0
fi

[ ${#ARGS[@]} -gt 0 ] || die "Give a color: preset (--list), #rrggbb, or R G B (0-255)"

# --- parse color ---
if [ ${#ARGS[@]} -eq 1 ]; then
  name="${ARGS[0],,}"
  if [ -n "${PRESETS[$name]}" ]; then
    read -r R G B <<< "${PRESETS[$name]}"
  else
    h="${name#\#}"
    [[ "$h" =~ ^[0-9a-f]{6}$ ]] || die "Bad color: ${ARGS[0]}"
    R=$((16#${h:0:2})); G=$((16#${h:2:2})); B=$((16#${h:4:2}))
  fi
elif [ ${#ARGS[@]} -eq 3 ]; then
  R="${ARGS[0]}"; G="${ARGS[1]}"; B="${ARGS[2]}"
  for v in "$R" "$G" "$B"; do
    [[ "$v" =~ ^[0-9]+$ ]] && [ "$v" -le 255 ] || die "R G B must be numbers 0-255"
  done
else
  die "Give one color name / hex, or three numbers R G B"
fi

# --- backup ---
[ -f "$FILE" ] || [ -f "$BAK" ] || die "File not found: $FILE (run in its folder)"
if [ ! -f "$BAK" ]; then
  cp "$FILE" "$BAK" || die "Cannot create backup"
  echo "Backup saved: $BAK"
fi

SIZE=$(stat -c %s "$BAK")
[ $((SIZE % 16)) -eq 0 ] || die "Size $SIZE is not a multiple of 16; not plain ETC2 RGBA data."

# --- build one 16-byte block ---
hex() { printf '\\x%02x' "$1"; }
BLOCK=$(printf '\\xff\\x10\\x00\\x00\\x00\\x00\\x00\\x00')
BLOCK+=$(hex $((R & 248)))$(hex $((G & 248)))$(hex $((B & 248)))
BLOCK+=$(printf '\\x02\\x00\\x00\\x00\\x00')

TMP="$FILE.tmp.$$"
printf "$BLOCK" > "$TMP"

# double the block until large enough, then cut to exact size
while [ "$(stat -c %s "$TMP")" -lt "$SIZE" ]; do
  cat "$TMP" "$TMP" > "$TMP.2" && mv "$TMP.2" "$TMP"
done
head -c "$SIZE" "$TMP" > "$FILE"
rm -f "$TMP"

echo "OK: $FILE filled with color $R $G $B, $(stat -c %s "$FILE") bytes"
