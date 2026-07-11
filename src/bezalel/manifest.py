"""Keturah capability manifest for Bezalel — the LLM-callable interfaces.

``build_manifest()`` is the federation seam (FR-FAMILY-01): Tirzah's
``family_registry()`` aggregates it fail-soft, so Bezalel's primitives appear
in the family capability view and, with handlers wired, in the Keturah MCP
server's ``tools/list``. Phase 1 declares only the safe primitives; each
capability carries its blast-radius class so the gate policy (Phase 3) can key
off the manifest rather than trusting the model.
"""

from __future__ import annotations

from bezalel import __version__
from bezalel.primitives import BLAST_RADIUS


def build_manifest():
    """Bezalel's capability manifest (requires keturah)."""
    from keturah import capability, manifest

    return manifest(
        "bezalel",
        version=__version__,
        description="Self-extending reasoning engine: sandboxed primitives "
        "(files/exec/net/models) + a human-gated self-extension loop. Phase 1 "
        "exposes the safe file/HTML primitives only.",
        capabilities=[
            capability(
                "write_file",
                "Write text to a path inside the workspace root "
                f"(blast-radius: {BLAST_RADIUS['write_file']}).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "workspace-relative path"},
                        "content": {"type": "string"},
                    },
                    "required": ["path", "content"],
                },
            ),
            capability(
                "read_file",
                "Read a file from the workspace root or the read-allowlist "
                f"(blast-radius: {BLAST_RADIUS['read_file']}).",
                input_schema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            ),
            capability(
                "edit_file",
                "Exact-match replace within a workspace file; fails on absent "
                f"or non-unique match (blast-radius: {BLAST_RADIUS['edit_file']}).",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "old": {"type": "string"},
                        "new": {"type": "string"},
                    },
                    "required": ["path", "old", "new"],
                },
            ),
            capability(
                "parse_html",
                "Extract visible text from an HTML string (pure, no network).",
                input_schema={
                    "type": "object",
                    "properties": {"html": {"type": "string"}},
                    "required": ["html"],
                },
            ),
        ],
    )
