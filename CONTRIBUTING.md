# Contributing to Hanani

Hanani is early (v0.1 design). The most useful contributions right now are
**sharpening the philosophy, requirements, and architecture** — especially the
factor taxonomy, evidence-graph schema, and confidence methodology — before code
sets them in stone.

## Development

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

- Python 3.11+; source under `src/hanani/`, tests under `tests/`.
- Decisions are recorded (append-only) in `docs/architecture-decisions.md`.

## Principles a change must respect

From [`docs/philosophy.md`](docs/philosophy.md):

- **Reports are witnesses, not verdicts.** No single outlet is granted authority
  a priori.
- **Inspectable reasoning.** Every synthesis retains witnesses, factors, debate
  transcript, and rejected hypotheses.
- **Equal scrutiny.** Competing hypotheses receive identical pressure.
- **Permitted uncertainty.** Speculative conclusions must remain labelled as such.
- **No popularity weighting.** Confidence excludes outlet reach, institutional
  authority, and social signals.
- **Sibling composition.** Hanani orchestrates Milcah, Tirzah, Hoglah, Galeed;
  it does not reimplement them.

## Reporting

Feedback: <https://github.com/gellsmore-svg/Hanani/issues>.
Security: see [SECURITY.md](SECURITY.md).