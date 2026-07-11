# Security Policy

Bezalel is an early local-first research prototype whose *purpose* is to run
side-effecting primitives (files, and later execution, network, and package/
model mutation) under model direction. **Treat it as unsuitable for untrusted
network exposure, and never run it against a workspace you cannot afford to
lose**, until the sandbox (Phase 2) and gate policy (Phase 3) are in place and
tested.

## The safety model

Bezalel's containment rests on one invariant (INV-1, see `README.md`): a model's
output only becomes a *proposed Cairn step*; nothing touches the world except by
executing a step that passed validation + `allowed_tools` + a gate, inside the
sandbox, traced in Galeed. Every primitive carries a **blast-radius class**, and
`execute` / `network` / `env-mutate` primitives are gated by default;
`pip_install` / `ollama_pull` are gated unconditionally. Phase 1 ships only the
safe file/HTML primitives — no execution, no network.

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

Report privately via GitHub's
[private vulnerability reporting](https://github.com/gellsmore-svg/Bezalel/security/advisories/new).

A sandbox-escape, a jail-escape in `Workspace`, or any path by which model text
reaches a side effect without passing INV-1 is the highest-severity class of bug
here — report those first.
