"""Phase-1 primitives: safe hands, jailed and deterministic."""

from __future__ import annotations

import pytest

from bezalel.cli import main
from bezalel.primitives import BLAST_RADIUS, edit_file, parse_html, read_file, write_file
from bezalel.workspace import Workspace, WorkspaceError


def test_write_read_roundtrip(tmp_path):
    ws = Workspace(tmp_path)
    write_file(ws, "notes/a.txt", "hello")
    assert read_file(ws, "notes/a.txt") == "hello"


def test_write_escape_blocked(tmp_path):
    ws = Workspace(tmp_path)
    with pytest.raises(WorkspaceError):
        write_file(ws, "../evil.txt", "x")


def test_edit_requires_unique_match(tmp_path):
    ws = Workspace(tmp_path)
    write_file(ws, "f.txt", "one two two")
    with pytest.raises(ValueError, match="not unique"):
        edit_file(ws, "f.txt", "two", "three")
    with pytest.raises(ValueError, match="not found"):
        edit_file(ws, "f.txt", "zzz", "y")
    edit_file(ws, "f.txt", "one", "1")
    assert read_file(ws, "f.txt") == "1 two two"


def test_parse_html_strips_tags_and_scripts():
    html = "<html><body><script>evil()</script><p>Hello <b>world</b></p></body></html>"
    assert parse_html(html) == "Hello world"


def test_blast_radius_declared_for_every_primitive():
    assert set(BLAST_RADIUS) == {"write_file", "read_file", "edit_file", "parse_html"}
    assert BLAST_RADIUS["write_file"] == "workspace-write"
    assert BLAST_RADIUS["parse_html"] == "pure"


def test_cli_roundtrip(tmp_path, capsys):
    assert main(["--workspace", str(tmp_path), "write", "x.txt", "data"]) == 0
    capsys.readouterr()
    assert main(["--workspace", str(tmp_path), "read", "x.txt"]) == 0
    assert capsys.readouterr().out == "data"
