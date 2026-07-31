"""Bezalel — a self-extending reasoning engine.

A local-first *maker*: a small set of side-effecting primitives (files,
execution, network, models) plus a self-extension loop, driven by the family's
bounded orchestration (Deborah plans + validation + gates + Galeed trace).

Phase 1 (this release) ships only the **deterministic substrate floor**: the
workspace jail and the safe primitives (write/read/edit/parse). Nothing here
executes a command, opens a socket, or calls a model — those arrive behind the
sandbox (Phase 2) and the gate policy (Phase 3). See ``docs/requirements.md``
(REQ-BEZALEL-001) and the family invariant INV-1: *models propose Deborah steps;
the substrate disposes.*
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as _pkg_version

from bezalel.primitives import edit_file, parse_html, read_file, write_file
from bezalel.workspace import Workspace, WorkspaceError

try:
    # Single source of truth: read the installed distribution rather than
    # restating the version here, so it cannot drift from pyproject.
    __version__ = _pkg_version("bezalel")
except PackageNotFoundError:  # running straight from a source checkout
    __version__ = "0.0.0+source"

__all__ = [
    "__version__",
    "Workspace",
    "WorkspaceError",
    "write_file",
    "read_file",
    "edit_file",
    "parse_html",
]
