<!-- managed-by: SBM-SUITE/context/scripts/suite-artifacts.py -->
# Transversal governance contract

This repository participates in the governance workflows controlled from
`SBM-SUITE/context`.

- Physical repository inventory is discovered by `scripts/suite-repositories.py`
  in the Context control plane.
- Multi-repository Git mutations are initiated only from `SBM-SUITE/context`.
- `main` is stable/release state and `develop` is integration state.
- `FEATURE-*` and `BUGFIX-*` branch from and integrate into `develop`.
- `RELEASE-*` branches from `develop`, integrates into `main`, then synchronizes
  `main` back into `develop`.
- `HOTFIX-*` branches from `main`, integrates into `main`, then synchronizes
  `main` back into `develop`.
- Release/main promotion follows `Development -> QA -> Security -> Release`.
  Rejection by Security returns work to Development and repeats QA and Security.
- Project-specific Context and QA content remains owned by this repository and
  must not be overwritten by transversal propagation.

This file is managed as a complete common artifact. Update its declared source
in `SBM-SUITE/context`, inspect with `suite-artifacts.py check`, and propagate
with an explicit `suite-artifacts.py apply` operation.
