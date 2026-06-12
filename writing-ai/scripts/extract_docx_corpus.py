#!/usr/bin/env python3
"""Extract readable text from every DOCX file in a folder using stdlib only."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PARAGRAPH = f"{{{W_NS}}}p"
TEXT = f"{{{W_NS}}}t"
TAB = f"{{{W_NS}}}tab"
BREAK = f"{{{W_NS}}}br"


def extract_paragraphs(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        xml_data = archive.read("word/document.xml")

    root = ET.fromstring(xml_data)
    paragraphs: list[str] = []
    for paragraph in root.iter(PARAGRAPH):
        parts: list[str] = []
        for node in paragraph.iter():
            if node.tag == TEXT and node.text:
                parts.append(node.text)
            elif node.tag == TAB:
                parts.append("\t")
            elif node.tag == BREAK:
                parts.append("\n")
        text = "".join(parts).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def find_documents(source: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in source.rglob("*.docx")
            if path.is_file() and not path.name.startswith("~$")
        ),
        key=lambda path: str(path).casefold(),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_dir():
        parser.error(f"Source folder does not exist: {source}")

    documents = find_documents(source)
    if not documents:
        parser.error(f"No DOCX files found in: {source}")

    sections: list[str] = ["# Writing corpus", "", f"Source: {source}", ""]
    failures: list[dict[str, str]] = []
    extracted = 0
    character_count = 0

    for document in documents:
        relative_name = document.relative_to(source)
        try:
            paragraphs = extract_paragraphs(document)
        except (KeyError, OSError, ET.ParseError, zipfile.BadZipFile) as error:
            failures.append({"file": str(relative_name), "error": str(error)})
            continue

        text = "\n\n".join(paragraphs)
        sections.extend([f"## {relative_name}", "", text, ""])
        extracted += 1
        character_count += len(text)

    if extracted == 0:
        print(json.dumps({"error": "No readable DOCX files", "failures": failures}, ensure_ascii=False))
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "source": str(source),
                "output": str(output),
                "documents_found": len(documents),
                "documents_extracted": extracted,
                "characters": character_count,
                "failures": failures,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

