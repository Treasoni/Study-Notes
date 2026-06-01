#!/usr/bin/env python3
"""Merge multiple doc-NN.md files into a single output file with HTML comment separators."""

import argparse
import os
import re
import sys


def read_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from content.

    Returns a dict of frontmatter fields, or empty dict if none found.
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    fm_text = match.group(1)
    result = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = value.strip()
    return result


def merge_files(input_dir: str, output_file: str, fmt: str = "html-comment") -> dict:
    """Merge all .md files from input_dir into output_file.

    Returns stats dict with keys: total_files, merged, skipped_empty, skipped_failed.
    """
    stats = {"total_files": 0, "merged": 0, "skipped_empty": 0, "skipped_failed": 0}

    if not os.path.isdir(input_dir):
        return stats

    md_files = sorted(f for f in os.listdir(input_dir) if f.endswith(".md"))
    stats["total_files"] = len(md_files)

    if not md_files:
        return stats

    sections = []
    for filename in md_files:
        filepath = os.path.join(input_dir, filename)
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Skip empty / whitespace-only files
        if not content.strip():
            stats["skipped_empty"] += 1
            continue

        # Skip files with status: failed in frontmatter
        fm = read_frontmatter(content)
        if fm.get("status") == "failed":
            stats["skipped_failed"] += 1
            continue

        # Extract URL for header comment
        url = fm.get("source_url", "unknown")

        # Build section
        # Strip leading/trailing whitespace from content for clean output
        body = content.strip()
        section = f"<!-- SOURCE: {filename} | url: {url} -->\n{body}\n<!-- END: {filename} -->"
        sections.append(section)
        stats["merged"] += 1

    if not sections:
        return stats

    merged = "\n\n".join(sections) + "\n"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(merged)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple doc-NN.md files into a single output file."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing doc-NN.md files",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for merged content",
    )
    parser.add_argument(
        "--format",
        default="html-comment",
        choices=["html-comment"],
        help="Output format (default: html-comment)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: input directory does not exist: {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    stats = merge_files(args.input_dir, args.output, args.format)

    if stats["merged"] == 0:
        print(
            f"Error: no valid files to merge in {args.input_dir} "
            f"(total={stats['total_files']}, empty={stats['skipped_empty']}, "
            f"failed={stats['skipped_failed']})",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"Merged {stats['merged']} file(s) -> {args.output} "
        f"(skipped: {stats['skipped_empty']} empty, {stats['skipped_failed']} failed)"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
