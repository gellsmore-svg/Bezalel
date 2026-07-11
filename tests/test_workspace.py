"""The jail must fail closed (FR-SANDBOX-01) — the floor of the safety story."""

from __future__ import annotations

import pytest

from bezalel.workspace import Workspace, WorkspaceError


def test_write_within_root_ok(tmp_path):
    ws = Workspace(tmp_path)
    resolved = ws.resolve_write("sub/dir/file.txt")
    assert str(resolved).startswith(str(tmp_path.resolve()))


@pytest.mark.parametrize("bad", ["../escape.txt", "sub/../../escape.txt", "/etc/passwd"])
def test_write_escape_rejected(tmp_path, bad):
    ws = Workspace(tmp_path)
    with pytest.raises(WorkspaceError):
        ws.resolve_write(bad)


def test_symlink_escape_rejected(tmp_path):
    root = tmp_path / "root"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "link").symlink_to(outside)  # a symlink pointing out of the jail
    ws = Workspace(root)
    with pytest.raises(WorkspaceError):
        ws.resolve_write("link/loot.txt")


def test_read_allowlist(tmp_path):
    root = tmp_path / "root"
    allowed = tmp_path / "reference"
    allowed.mkdir()
    (allowed / "note.txt").write_text("ok", encoding="utf-8")
    ws = Workspace(root, read_allowlist=[str(allowed)])
    assert ws.resolve_read(str(allowed / "note.txt"))
    with pytest.raises(WorkspaceError):
        ws.resolve_read("/etc/hosts")
    # writes are never widened by the read-allowlist
    with pytest.raises(WorkspaceError):
        ws.resolve_write(str(allowed / "note.txt"))
