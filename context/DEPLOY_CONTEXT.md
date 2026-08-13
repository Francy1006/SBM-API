# DEPLOY_CONTEXT.md

> **Last updated:** 2026-08-13
>
> **Purpose:** Canonical deployment/lifecycle context for SBM-API.
>
> **Accuracy note:** Runtime facts are derived from the supplied repository. This document does not claim a deployment, Context upgrade, Documentation upgrade or QA execution that was not actually performed.

## 1. Scope and ownership

SBM-API project deployment/runtime configuration is owned by this repository. Suite Context and Documentation lifecycle orchestration is owned globally by `SBM-SUITE/context`.

## 2. Required configuration

Development/runtime configuration:

```text
.env.dev
```

Required categories include Django runtime, PostgreSQL connectivity, Suite lifecycle routing and SonarQube configuration. Secret values must never be embedded in this file or lifecycle packages.

## 3. Canonical paths

```text
registry_project_name: sbm-api
repository path: SBM-SUITE/sbm/SBM-API/
runtime root: /suite/sbm/SBM-API
project context: SBM-SUITE/sbm/SBM-API/context/
global context: SBM-SUITE/context/
```

Current physical developer workspaces may preserve group-directory casing such as `SBM/`; backend lifecycle manifests use the canonical registry mapping above.

## 4. Context deploy workflow

Execute from the root of:

```text
SBM-SUITE/context
```

Use the global lifecycle script and literal backend registry name:

```text
./scripts/context-deploy.sh "sbm-api" <lifecycle-phase> '<objectives-json-array>'
```

Project-local `context-deploy.sh` wrappers are intentionally not required by the current governance model.

## 5. Manual review stage

Generated Context packages are reviewed by ChatGPT under the current `SYS_PROMPT.md`/`FORMAT_CONTEXT.md` contract before any upgrade is applied.

Never hand-edit generated ZIP contents, manifests or patches to bypass a lifecycle failure.

## 6. Context upgrade workflow

Context upgrades are executed only from:

```text
SBM-SUITE/context
```

Canonical command:

```text
./scripts/context-upgrade.sh
```

The backend response is the authority for `updated_files`, errors and whether Context source-of-truth actually changed.

## 7. Atomicity and cleanup

- Treat generated lifecycle packages as immutable evidence.
- Apply upgrades through the global validated scripts only.
- Successful global upgrade scripts own cleanup of their exchange directories.
- Never manually patch ZIPs to recover from failed validation.
- Preserve unrelated user working-tree changes.

## 8. Rollback

Use Git history and Context-generated backup artifacts when an applied lifecycle change must be reverted. Do not reset or overwrite unrelated repository changes.

Runtime rollback must be based on explicit deployment evidence; no production rollback procedure is inferred by this baseline.

## 9. Validation performed

For this integration package:

```text
repository structure inspected
Docker Compose service/ports inspected
Django settings/routes inspected
backend registry mapping verified from supplied Suite reference evidence
shell scripts syntax-validated before delivery
no runtime Docker/DB/Sonar execution claimed
```

## 10. Current limitations

- Current global Context state in this conversation may be older than the user's latest lifecycle reconciliation and is not overwritten by this package.
- Automated QA baseline is pending.
- Production deployment/hardening is outside this package.
- Database mapping validation against current SBM-DB/Flyway remains pending.
