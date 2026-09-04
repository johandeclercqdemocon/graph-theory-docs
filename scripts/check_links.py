"""Check that every relative link in the book resolves to a file that exists.

    python scripts/check_links.py

Mechanical and zero-false-positive: it resolves each relative markdown link
against the containing file's directory and reports the ones that do not exist.
External links are not fetched -- that would need the network, which nothing
else in this book requires.

This exists because the README listed three appendices before they were written,
and the chapters all link to Appendix E. A dead link in a finished book is a
defect, and it is the kind that is invisible until someone clicks.
"""

from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)#]+?)(?:#[^)]*)?\)")
SKIP = {".git", ".venv", "__pycache__", "node_modules"}


def main() -> int:
    checked = 0
    broken: list[str] = []
    for md in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP for part in md.parts):
            continue
        for link in LINK.findall(md.read_text()):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            if not (md.parent / link).resolve().exists():
                broken.append(f"{md.relative_to(ROOT)} -> {link}")

    print(f"  {checked} relative links checked")
    if broken:
        print(f"\n{len(broken)} broken:\n")
        for b in broken:
            print("  " + b)
        return 1
    print("\nAll links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
