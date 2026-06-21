#!/usr/bin/env bash
# Thin launcher — all logic lives in update.py (next to this file). Double-click to update.
set -u
cd "$(dirname "$0")"

echo "MedSci Skills Updater for macOS"
echo

if command -v python3 >/dev/null 2>&1; then
  python3 update.py "$@"
  rc=$?
elif command -v python >/dev/null 2>&1; then
  python update.py "$@"
  rc=$?
else
  echo "Python 3 was not found."
  echo "Install Python 3 from https://www.python.org/downloads/ and run this updater again."
  rc=1
fi

echo
read -r -p "Press Enter to close..."
exit $rc
