"""The workspace jail (FR-SANDBOX-01).

Every file primitive is confined to a configured **workspace root**. Path
traversal, absolute escape, and symlink escape are rejected *before* any I/O —
fail closed. This module is pure deterministic Python and is unit-tested
without any model (NFR-DETERMINISTIC-SUBSTRATE): it is the floor the whole
safety story stands on.

Reads *may* be widened to an explicit allow-list of paths outside the root
(FR-PRIM-02); writes never leave the root.
"""

from __future__ import annotations

import os
from pathlib import Path


class WorkspaceError(Exception):
    """A path escaped the workspace jail (or a read-allowlist)."""


class Workspace:
    """A path-jailed root for Bezalel's file primitives.

    :param root: the directory all writes/reads are confined to (created if
        missing).
    :param read_allowlist: extra paths (files or directories) that
        :meth:`resolve_read` will also permit, for reading only.
    """

    def __init__(
        self, root: str | os.PathLike[str], *, read_allowlist: list[str] | None = None
    ) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self._read_allow = [Path(p).resolve() for p in (read_allowlist or [])]

    # -- internals -----------------------------------------------------------

    def _within(self, candidate: Path, base: Path) -> bool:
        try:
            candidate.relative_to(base)
        except ValueError:
            return False
        return True

    def _resolve_symlink_safe(self, path: Path) -> Path:
        """Resolve a path guarding against symlink escape.

        We resolve the *nearest existing ancestor* (following symlinks) and
        re-attach the remaining tail, so a symlink anywhere along an existing
        prefix cannot smuggle the target outside the jail.
        """
        raw = (self.root / path) if not path.is_absolute() else path
        existing = raw
        tail: list[str] = []
        while not existing.exists():
            tail.append(existing.name)
            existing = existing.parent
        resolved = existing.resolve()
        for part in reversed(tail):
            resolved = resolved / part
        # the existing ancestor is symlink-resolved; the non-existent tail may
        # still carry ".." — collapse it lexically so it cannot escape the jail.
        return Path(os.path.normpath(resolved))

    # -- public --------------------------------------------------------------

    def resolve_write(self, path: str | os.PathLike[str]) -> Path:
        """Return the absolute path for a write, or raise if it escapes root."""
        resolved = self._resolve_symlink_safe(Path(path))
        if not self._within(resolved, self.root):
            raise WorkspaceError(f"path escapes workspace root: {path!r}")
        return resolved

    def resolve_read(self, path: str | os.PathLike[str]) -> Path:
        """Return the absolute path for a read (root or an allowlisted path)."""
        resolved = self._resolve_symlink_safe(Path(path))
        if self._within(resolved, self.root):
            return resolved
        for allowed in self._read_allow:
            if resolved == allowed or self._within(resolved, allowed):
                return resolved
        raise WorkspaceError(f"path is outside workspace and read-allowlist: {path!r}")
