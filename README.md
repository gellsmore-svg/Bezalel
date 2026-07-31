# Bezalel

*"Filled with skill to make all manner of workmanship."* (Exodus 31)

**Bezalel** is a local-first, self-extending reasoning engine. It exposes a
small set of side-effecting primitives — files, execution, network, models —
and a **human-gated self-extension loop** that lets it author, test, and
register *new* capabilities for itself and the family. It is a *maker*, not a
general coding agent (that is Codex + the family surround).

Its reasoning is not a bespoke agent loop: work runs as a **Deborah plan** that
the family's interpretive planner validates and gates before any primitive
touches the world, with every step traced to **Galeed** and browsable in
**Mizpah**.

## The invariant (INV-1)

> A model's output only ever becomes a **proposed Deborah step**. Nothing touches
> the filesystem, network, or package/model state except by executing a step
> that passed `deborah.validate_plan` + its `allowed_tools` constraint + its
> governance gate, **inside the sandbox**, **traced in Galeed**.

Everything below is subordinate to that line: *models propose, the substrate
disposes.*

## Status — Phase 1 (deterministic substrate floor)

This release ships only the safe, offline floor:

| Primitive | Blast radius | Ships |
|---|---|---|
| `write_file` / `read_file` / `edit_file` | workspace-write / read | ✅ Phase 1 |
| `parse_html` | pure | ✅ Phase 1 |
| `run` | execute | ⏳ Phase 2 (sandbox) |
| `call_model` (via Hoglah) | model | ⏳ Phase 3 |
| `browse` | network | ⏳ Phase 5 |
| `pip_install` / `ollama_pull` | env-mutate | ⏳ Phase 5 (hard-gated) |

Nothing here runs a command, opens a socket, or calls a model. The
[workspace jail](src/bezalel/workspace.py) is the floor the whole safety story
stands on, and it fails closed.

## Try it

```bash
pip install -e ".[dev]"
bezalel --workspace /tmp/ws write notes/hello.txt "hi"
bezalel --workspace /tmp/ws read notes/hello.txt
pytest -q
```

## Design

- [`docs/requirements.md`](docs/requirements.md) — REQ-BEZALEL-001, the
  normative requirements (INV-1, FR-PRIM/SANDBOX/PLAN/EXT/GATE/TRACE/FAMILY,
  the 5-phase plan).

## Family

Bezalel federates through **Keturah** (`build_manifest()`), calls models
through **Hoglah**, traces to **Galeed**, and is reasoned by **Tirzah**'s
planner over **Deborah** plans. It is one specialist — the *builder* — in the
family's distributed intelligence.
