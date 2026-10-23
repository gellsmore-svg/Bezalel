# Bezalel

**Bezalel is a local reasoning engine designed to safely build new
capabilities for itself, with a human approving each one.** It works through
a small set of side-effecting primitives (files, execution, network, models),
and every action a model proposes must pass validation, a governance gate and
a sandbox before it touches anything.

It is a *maker*, not a general coding agent. The name is from Exodus 31:
*"filled with skill to make all manner of workmanship."*

## Status: Phase 1 of 5

**Today Bezalel is the safe, offline floor only.** It has workspace-jailed
file primitives and HTML parsing, driven from a CLI. Nothing in this release
runs a command, opens a socket or calls a model.

| Primitive | Blast radius | Ships in |
|---|---|---|
| `write_file` / `read_file` / `edit_file` | workspace write / read | ✅ Phase 1 |
| `parse_html` | pure | ✅ Phase 1 |
| `run` | execute | Phase 2 (sandbox) |
| `call_model` (via Hoglah) | model | Phase 3 |
| `browse` | network | Phase 5 |
| `pip_install` / `ollama_pull` | environment mutation, hard-gated | Phase 5 |

The [workspace jail](src/bezalel/workspace.py) is what the whole safety story
stands on. It fails closed: paths that escape the workspace, symlinks and
hard links are refused.

## Try it

```bash
pip install bezalel-engine           # not "bezalel": that PyPI name belongs to another project
bezalel --workspace /tmp/ws write notes/hello.txt "hi"
bezalel --workspace /tmp/ws read notes/hello.txt
bezalel --workspace /tmp/ws edit notes/hello.txt "hi" "hello"
bezalel --workspace /tmp/ws parse-html page.html
```

## The design rule (INV-1)

> A model's output only ever becomes a **proposed Deborah step**. Nothing
> touches the filesystem, network, or package or model state except by
> executing a step that passed `deborah.validate_plan`, its `allowed_tools`
> constraint and its governance gate, **inside the sandbox**, **traced in
> Galeed**.

*Models propose; the substrate disposes.* This is the rule every later phase
is built to. **In Phase 1 the plan path does not exist yet.** The CLI calls
the primitives directly, and the workspace jail is the only guard. Model
proposals, plan validation and the gates arrive with Phases 2–3.

## Where it fits in the family

| Bezalel uses | For | Today |
|---|---|---|
| [Keturah](https://github.com/gellsmore-svg/keturah) | its capability manifest (`bezalel.manifest.build_manifest()`) | ✅ |
| [Galeed](https://github.com/gellsmore-svg/galeed) | a `bezalel.<primitive>` event per call | ⚠️ emitted in-process but not yet stored, so not visible in Mizpah |
| [Deborah](https://github.com/gellsmore-svg/Deborah) | plans that validate every model-proposed step | Phase 2+ |
| [Hoglah](https://github.com/gellsmore-svg/hoglah) | model calls | Phase 3 |
| [Tirzah](https://github.com/gellsmore-svg/tirzah) | the planner that reasons over Deborah plans | Phase 2+ |

## Design and development

- [docs/requirements.md](docs/requirements.md): REQ-BEZALEL-001, the
  normative requirements (INV-1, primitives, sandbox, plans, self-extension,
  gates, tracing, family integration) and the five-phase plan.
- Develop: `pip install -e ".[dev]" && pytest -q`.

[CONTRIBUTING](CONTRIBUTING.md) · [SECURITY](SECURITY.md) · [LICENSE](LICENSE)
