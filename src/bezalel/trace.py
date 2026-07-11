"""Galeed trace seam (FR-TRACE-01) — every primitive emits an event.

Fail-soft, like the other siblings: if Galeed is not installed the emit is a
no-op, so the substrate runs standalone. When present, each primitive call
becomes a browsable ``bezalel.<primitive>`` event in Mizpah, carrying inputs
(redacted as needed), the outcome, and any sandbox flags.
"""

from __future__ import annotations

from typing import Any


def emit(event: str, *, trace_id: str = "bezalel", summary: str = "", **fields: Any) -> None:
    """Emit a Galeed event; a no-op when Galeed is unavailable."""
    try:
        from galeed import Tracer  # type: ignore
    except Exception:  # noqa: BLE001 - trace is best-effort, never fatal
        return
    try:
        Tracer(trace_id=trace_id, session_id="bezalel", source="bezalel").emit(
            event, summary=summary, **fields
        )
    except Exception:  # noqa: BLE001
        return
