"""The manifest is the federation seam and the gate policy's source of truth."""

from __future__ import annotations

import pytest

from bezalel.primitives import BLAST_RADIUS


def test_manifest_declares_every_phase1_primitive():
    pytest.importorskip("keturah")
    from bezalel.manifest import build_manifest

    m = build_manifest()
    names = {c.name for c in m.capabilities}
    assert names == set(BLAST_RADIUS), "every primitive must be manifested"
