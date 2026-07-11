"""Minimal CLI for the Phase-1 primitives.

Deliberately thin: the real driver is the family planner (FR-PLAN, Phase 3).
This exists so the substrate is exercisable by hand and in CI.
"""

from __future__ import annotations

import argparse
import sys

from bezalel import __version__
from bezalel.primitives import edit_file, parse_html, read_file, write_file
from bezalel.workspace import Workspace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="bezalel", description="Bezalel primitives")
    parser.add_argument("--version", action="version", version=f"bezalel {__version__}")
    parser.add_argument("--workspace", default=".", help="workspace root")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_write = sub.add_parser("write", help="write a file")
    p_write.add_argument("path")
    p_write.add_argument("content")

    p_read = sub.add_parser("read", help="read a file")
    p_read.add_argument("path")

    p_edit = sub.add_parser("edit", help="exact-match edit a file")
    p_edit.add_argument("path")
    p_edit.add_argument("old")
    p_edit.add_argument("new")

    p_parse = sub.add_parser("parse-html", help="extract text from an HTML file")
    p_parse.add_argument("path")

    args = parser.parse_args(argv)
    ws = Workspace(args.workspace)

    if args.cmd == "write":
        print(write_file(ws, args.path, args.content))
    elif args.cmd == "read":
        print(read_file(ws, args.path), end="")
    elif args.cmd == "edit":
        print(edit_file(ws, args.path, args.old, args.new))
    elif args.cmd == "parse-html":
        print(parse_html(read_file(ws, args.path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
