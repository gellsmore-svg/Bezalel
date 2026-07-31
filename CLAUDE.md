# Bezalel — working notes

Self-extending reasoning engine. A *maker*: sandboxed primitives + a
human-gated self-extension loop, reasoned by the family planner (not a bespoke
agent loop). See `docs/requirements.md` (REQ-BEZALEL-001) and INV-1 in the
README — everything is subordinate to *models propose, the substrate disposes*.

## Scoreboard

**Implemented (Phase 1 — deterministic floor):**
- `workspace.py` — the path jail (FR-SANDBOX-01), fails closed incl. symlink
  escape; pure, model-free, the floor of the safety story.
- `primitives.py` — `write_file` / `read_file` / `edit_file` / `parse_html`
  (FR-PRIM-01/02/03/06), each jailed + Galeed-traced; `BLAST_RADIUS` map.
- `trace.py` — fail-soft Galeed emit (FR-TRACE-01).
- `manifest.py` — Keturah federation seam (FR-FAMILY-01), declares the four
  safe primitives with blast-radius in the description.
- `cli.py` — thin hand-driver; tests green, ruff clean.

**Scaffold / declared, not built:**
- Nothing higher than the safe primitives. No `run`, no network, no model call.

**Planned (next, in order):**
1. **Phase 2 — `run` under a sandbox.** Reuse Codex's `bwrap`/`linux-sandbox`
   (already on the dev box); workspace bind-mount only, network off, resource
   caps; `FR-SANDBOX-02/04`. This is the autonomy gate — do it deliberately.
2. **Phase 3 — Deborah-planned reasoning.** Wire Tirzah's planner with
   `allowed_tools` = Bezalel primitives; class-based gate policy keyed off the
   manifest; arm the outcomes loop by default; ack semantics (FR-PLAN, FR-GATE).
3. **Phase 4 — self-extension.** author → test-in-sandbox → human gate →
   register; no-core-mutation guard (FR-EXT).
4. **Phase 5 — reach out.** `browse` (allowlist), `pip_install` / `ollama_pull`
   (pinned, hard-gated) (FR-PRIM-05/08/09, FR-SANDBOX-03).

## Conventions (family standard)
- Deterministic substrate is pure Python, unit-tested with **no model**.
- Model tiers are injectable and validated against a closed vocabulary; never
  auto-act on a model alone.
- `pip install -e ".[dev]"`; `ruff check src tests`; `pytest -q`. CI matrix 3.11/3.12.
- Federates via Keturah; models via Hoglah; traces to Galeed; reasoned by Tirzah/Deborah.
