#!/usr/bin/env python3
"""Say What Actually Broke — entry program.

Writes exactly one line of error copy to /output/entry.txt.
Deterministic: fixed text, no randomness, no clock, no network,
Python standard library only.
"""

import os
import sys

LINE = (
    "Your save failed: our database ran out of disk space, "
    "choked on three years of logs nobody ever reads. "
    "Your work is safe \u2014 our housekeeping is not."
)

OUT_DIR = "/output"
OUT_FILE = os.path.join(OUT_DIR, "entry.txt")
MAX_CHARS = 200


def check(text):
    """Gate: one non-blank line, 1-200 characters."""
    if not text.strip():
        raise SystemExit("error: entry line is blank")
    if len(text) > MAX_CHARS:
        raise SystemExit("error: entry line exceeds 200 characters")
    if any(c in text for c in "\r\n"):
        raise SystemExit("error: entry line must be a single line")


def clear_output_dir():
    os.makedirs(OUT_DIR, exist_ok=True)
    for entry in os.scandir(OUT_DIR):
        if entry.is_file(follow_symlinks=False) or entry.is_symlink():
            os.unlink(entry.path)


def write_entry():
    check(LINE)
    clear_output_dir()
    with open(OUT_FILE, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")
    os.chmod(OUT_FILE, 0o644)


def verify_written():
    """Read back what was written and re-apply the gate."""
    with open(OUT_FILE, "r", encoding="utf-8") as handle:
        written = handle.read()
    if not written.endswith("\n"):
        raise SystemExit("error: output does not end with a newline")
    check(written.rstrip("\n"))


def run():
    write_entry()
    verify_written()
    return 0


if __name__ == "__main__":
    sys.exit(run())
