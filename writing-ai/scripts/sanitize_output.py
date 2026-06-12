#!/usr/bin/env python3
"""Remove or detect double quotation marks and dash punctuation in prose."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FORBIDDEN = ('"', "“", "”", "—", "–", "―", "⸺", "⸻")


def sanitize(text: str) -> str:
    for character in FORBIDDEN:
        text = text.replace(character, "")
    text = re.sub(r"-{2,}", "", text)
    return text


def violations(text: str) -> list[str]:
    found = [character for character in FORBIDDEN if character in text]
    if re.search(r"-{2,}", text):
        found.append("repeated ASCII hyphens")
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    if args.check:
        found = violations(text)
        if found:
            print("Forbidden punctuation found: " + ", ".join(found), file=sys.stderr)
            return 1
        print("OK: no forbidden punctuation found")
        return 0

    cleaned = sanitize(text)
    target = args.output or args.input
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(cleaned, encoding="utf-8")
    print(f"Sanitized output written to: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
