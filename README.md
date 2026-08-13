# SBM-API

## Role within SBM Suite

SBM-API is the internal platform API of SBM Suite. It owns platform and administrative operations that must not be exposed through the client-facing DP-API boundary.

Canonical Suite identity:

```text
registry_project_name: sbm-api
repository root: SBM-SUITE/sbm/SBM-API/
runtime root: /suite/sbm/SBM-API
```

## Project status

The supplied repository is an active Django REST Framework application. It exposes the local API on host port `8082`, uses PostgreSQL through `sbm-network`, and contains current domain modules for platform operations.

Project-level Context/QA/Sonar integration is provided by this repository. Global Context and Documentation lifecycle commands are executed from `SBM-SUITE/context`.

## Technology stack

- Python 3.9 container runtime
- Django 4.2.7
- Django REST Framework 3.14
- PostgreSQL
- Docker Compose
- coverage.py
- pytest / pytest-django available
- SonarQube via containerized SonarScanner

## Current app ownership

Current Django apps include:

```text
accounting
calculation
catalog
clients
config
fiscal
franchise
inventory
module
price
sales
support
users
```

The API owns internal/platform application behavior. Physical schema evolution remains owned by SBM-DB/Flyway where that ownership applies.

## Architecture

```text
SBM-MANAGER / internal consumers
            ↓
         SBM-API
            ↓
 Django REST Framework
            ↓
      PostgreSQL
            ↑
     SBM-DB / Flyway
```

The current Django database search path is:

```text
sbm_business, ditaly_pasta, analytics, public
```

## Database ownership

SBM-API contains both managed and unmanaged Django models. Unmanaged mappings must remain aligned with the canonical PostgreSQL/Flyway schema and must not be treated as physical schema authority.

Do not create database migrations merely to reconcile an unmanaged model with the database.

## Requirements

- Docker
- Docker Compose
- external Docker network `sbm-network`
- PostgreSQL reachable with the configured `.env.dev` values
- SonarQube only when running final QA

## Environment configuration

Development configuration is loaded from:

```text
.env.dev
```

Relevant variable names include:

```text
DEBUG
SECRET_KEY
ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
DOPPLER_PROJECT
AI_ASSISTANT_URL
SBM_SUITE_ROOT
SONAR_HOST_URL
SONAR_API_URL
SONAR_TOKEN
```

Never commit environment files or secret values.

## Build and start

```bash
docker compose --env-file .env.dev build api
docker compose --env-file .env.dev up api
```

## Runtime operations

Django validation:

```bash
docker compose --env-file .env.dev run --rm --no-deps --entrypoint python api manage.py check
```

Final project QA:

```bash
./scripts/qa-check.sh
```

## Local URLs

```text
Application: http://localhost:8082/
API root:    http://localhost:8082/api/
Health:      http://localhost:8082/api/health/
Info:        http://localhost:8082/api/info/
Admin:       http://localhost:8082/admin/
Token auth:  http://localhost:8082/api-token-auth/
```

## Main REST resources

The repository routes platform modules below `/api/`, including franchise, catalog, accounting, support, pricing, sales, configuration, fiscal, inventory, clients, calculation, module and users.

Exact endpoint behavior remains owned by each app's `urls.py`, views and serializers.

## Usage examples

Health check:

```bash
curl http://localhost:8082/api/health/
```

API inventory:

```bash
curl http://localhost:8082/api/
```

## Authentication and authorization

The repository exposes Django/DRF session authentication and token authentication. Authorization and tenant/franchise boundaries must be validated per endpoint; existence of authentication middleware does not by itself prove complete object-level authorization.

## Administration

Django Admin is available at:

```text
/admin/
```

Administrative credentials are environment-managed and must not be stored in Git or Context artifacts.

## Reusable components

| File name | Path | Description |
|---|---|---|
| `settings.py` | `core/settings.py` | Django runtime, database, REST and CORS configuration |
| `urls.py` | `core/urls.py` | Root URL composition for platform APIs |
| `authentication.py` | `users/authentication.py` | Project authentication support |
| `coverage.sh` | `scripts/coverage.sh` | Containerized Django check, tests and coverage generation |
| `sonar-scan.sh` | `scripts/sonar-scan.sh` | SonarScanner execution and server-side Quality Gate validation |
| `qa-check.sh` | `scripts/qa-check.sh` | Complete QA evidence generation |

## QA and code quality

Repository QA is project-specific and produces:

```text
context/qa-results.md
```

Current supplied `tests.py` files are mostly baseline placeholders; no passing automated-test baseline is claimed by this integration.

Run final QA only after SonarQube is confirmed available:

```bash
./scripts/qa-check.sh
```

## SonarQube configuration

Project configuration:

```text
sonar-project.properties
Project key: SBM-API
Coverage report: coverage.xml
```

The scanner must validate the server-side Quality Gate before QA can be considered passed.

## AI integration

Canonical lifecycle routing already uses:

```text
sbm-api → /suite/sbm/SBM-API
```

Context and Documentation operations are executed from the global repository:

```text
SBM-SUITE/context
```

Project-local lifecycle wrappers are intentionally not required.

## Security

- Never commit `.env.dev`, `.env.prod`, tokens or credentials.
- Treat `SECRET_KEY`, database credentials and `SONAR_TOKEN` as secrets.
- Review `CORS_ALLOW_ALL_ORIGINS` before production use.
- Validate object-level authorization and tenant/franchise isolation explicitly.
- Do not package environment values into Context or Documentation artifacts.

## Project documentation

Canonical project context:

```text
context/PROJECT_CONTEXT.md
context/QA_CONTEXT.md
context/DEPLOY_CONTEXT.md
```

Global Suite context:

```text
SBM-SUITE/context/PROJECT_CONTEXT.md
SBM-SUITE/context/SUITE_CONTEXT.md
SBM-SUITE/context/QA_CONTEXT.md
```

## License

Private SBM Suite project unless a separate repository license states otherwise.

## Context lifecycle

Run Context and Documentation lifecycle commands only from:

```text
SBM-SUITE/context
```

The backend registry name is:

```text
sbm-api
```

Project implementation QA remains local to this repository through `scripts/qa-check.sh`.
