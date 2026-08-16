#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${ROOT}/.env.dev"
CONTAINER_NAME="sbm-api-qa-coverage"
COVERAGE_XML="${ROOT}/coverage.xml"

[[ -f "${ENV_FILE}" ]] || {
  echo "ERROR: No existe .env.dev" >&2
  exit 1
}

cleanup() {
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

cd "${ROOT}"
rm -f "${COVERAGE_XML}"
cleanup

docker compose --env-file "${ENV_FILE}" config -q

docker compose --env-file "${ENV_FILE}" run \
  --name "${CONTAINER_NAME}" \
  --no-deps \
  --entrypoint sh \
  api -lc '
set -eu
python manage.py check
coverage erase
TEST_OUTPUT="$(coverage run \
  --source=accounting,calculation,catalog,clients,config,core,fiscal,franchise,inventory,module,price,sales,support,users \
  manage.py test 2>&1)"
printf "%s\n" "$TEST_OUTPUT"

if printf "%s\n" "$TEST_OUTPUT" | grep -Eq "Found 0 test\(s\)|Ran 0 tests"; then
  echo "ERROR: SBM-API no tiene tests ejecutables" >&2
  exit 1
fi

coverage xml -o /tmp/coverage.xml
coverage report -m
'

docker cp "${CONTAINER_NAME}:/tmp/coverage.xml" "${COVERAGE_XML}" >/dev/null
[[ -s "${COVERAGE_XML}" ]] || {
  echo "ERROR: No se generó coverage.xml" >&2
  exit 1
}

echo "Coverage artifact: coverage.xml"
