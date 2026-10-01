#!/usr/bin/env bash
# Wrapper for photo2ubulk.py: installs what is needed (Termux) and runs it.
#
# Usage:
#   bash photo.sh photo.jpg
#   bash photo.sh photo.jpg --flipy
#   bash photo.sh --restore
#
# Put photo.sh, photo2ubulk.py and DesertHDRI.ubulk in the same folder.

DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$DIR/photo2ubulk.py"

[ -f "$SCRIPT" ] || { echo "photo2ubulk.py not found next to photo.sh" >&2; exit 1; }

if ! command -v python3 >/dev/null 2>&1 || \
   ! python3 -c "import numpy, PIL" >/dev/null 2>&1; then
  if command -v pkg >/dev/null 2>&1; then
    echo "Installing python, numpy, pillow ..."
    pkg install -y python python-numpy python-pillow || exit 1
  else
    echo "Need python3 with numpy and Pillow installed." >&2
    exit 1
  fi
fi

python3 "$SCRIPT" "$@"
