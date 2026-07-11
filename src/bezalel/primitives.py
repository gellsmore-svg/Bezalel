"""Phase-1 primitives: the safe, deterministic hands (FR-PRIM-01/02/03/06).

These are the primitives with the smallest blast radius — ``workspace-write``,
``read``, and ``pure`` — so they ship first, standalone, fully testable
offline. Each is jailed to a :class:`~bezalel.workspace.Workspace` and emits a
Galeed event. The higher-blast-radius primitives (``run``, ``browse``,
``call_model``, ``pip_install``, ``ollama_pull``) are deliberately absent until
the sandbox (Phase 2) and gate policy (Phase 3) exist — per INV-1, nothing
touches the world except through a validated, gated, sandboxed step.
"""

from __future__ import annotations

import re

from bezalel import trace
from bezalel.workspace import Workspace

# blast-radius class per primitive, the safety model's backbone (FR-PRIM).
BLAST_RADIUS = {
    "write_file": "workspace-write",
    "read_file": "read",
    "edit_file": "workspace-write",
    "parse_html": "pure",
}


def write_file(ws: Workspace, path: str, content: str) -> str:
    """Write ``content`` to ``path`` inside the workspace root (FR-PRIM-01)."""
    target = ws.resolve_write(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    trace.emit("bezalel.write_file", summary=str(path), bytes=len(content))
    return str(target)


def read_file(ws: Workspace, path: str) -> str:
    """Return the contents of ``path`` (root or read-allowlisted) (FR-PRIM-02)."""
    source = ws.resolve_read(path)
    content = source.read_text(encoding="utf-8")
    trace.emit("bezalel.read_file", summary=str(path), bytes=len(content))
    return content


def edit_file(ws: Workspace, path: str, old: str, new: str) -> str:
    """Exact-match replace ``old`` with ``new`` in a workspace file (FR-PRIM-03).

    Fails without writing if ``old`` is absent or non-unique — the same
    contract the family's Edit tool enforces, so edits stay unambiguous.
    """
    target = ws.resolve_write(path)
    content = target.read_text(encoding="utf-8")
    count = content.count(old)
    if count == 0:
        raise ValueError(f"old string not found in {path!r}")
    if count > 1:
        raise ValueError(f"old string is not unique in {path!r} ({count} matches)")
    target.write_text(content.replace(old, new), encoding="utf-8")
    trace.emit("bezalel.edit_file", summary=str(path))
    return str(target)


_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)


def parse_html(html: str) -> str:
    """Extract visible text from an HTML string (FR-PRIM-06, pure, no network).

    Prefers ``beautifulsoup4`` when installed; otherwise falls back to a
    tolerant regex strip so the primitive works with zero optional deps.
    """
    try:
        from bs4 import BeautifulSoup  # type: ignore

        text = BeautifulSoup(html, "html.parser").get_text(separator=" ")
    except Exception:  # noqa: BLE001 - fall back to dependency-free strip
        stripped = _SCRIPT_STYLE_RE.sub(" ", html or "")
        text = _TAG_RE.sub(" ", stripped)
    text = _WS_RE.sub(" ", text).strip()
    trace.emit("bezalel.parse_html", bytes=len(html or ""), chars=len(text))
    return text
