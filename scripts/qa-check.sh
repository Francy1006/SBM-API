#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RESULT_FILE="${ROOT}/context/qa-results.md"
COVERAGE_LOG="$(mktemp)"
SONAR_LOG="$(mktemp)"
trap 'rm -f "${COVERAGE_LOG}" "${SONAR_LOG}"' EXIT

mkdir -p "${ROOT}/context"

coverage_exit=0
"${SCRIPT_DIR}/coverage.sh" > >(tee "${COVERAGE_LOG}") 2>&1 || coverage_exit=$?

tests_total="$(python3 - "${COVERAGE_LOG}" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
patterns = [r"Found\s+(\d+)\s+test", r"Ran\s+(\d+)\s+test"]
for pattern in patterns:
    m = re.search(pattern, text)
    if m:
        print(m.group(1))
        break
else:
    print("0")
PY
)"

failed_tests="$(python3 - "${COVERAGE_LOG}" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
m = re.search(r"FAILED\s*\(([^)]*)\)", text)
if not m:
    print("0")
    raise SystemExit
count = 0
for key in ("failures", "errors", "unexpected successes"):
    x = re.search(rf"{re.escape(key)}=(\d+)", m.group(1))
    if x:
        count += int(x.group(1))
print(count)
PY
)"

if [[ "${coverage_exit}" -ne 0 && "${tests_total}" -gt 0 && "${failed_tests}" -eq 0 ]]; then
  failed_tests="${tests_total}"
fi
passed_tests=$(( tests_total > failed_tests ? tests_total - failed_tests : 0 ))

coverage_result="N/A"
if [[ -s "${ROOT}/coverage.xml" ]]; then
  coverage_result="$(python3 - "${ROOT}/coverage.xml" <<'PY'
import sys
import xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
rate = root.attrib.get("line-rate")
print(f"{float(rate) * 100:.2f}%" if rate is not None else "N/A")
PY
)"
fi

sonar_exit=0
scanner_result="not-run"
quality_gate="N/A"
if [[ "${coverage_exit}" -eq 0 ]]; then
  "${SCRIPT_DIR}/sonar-scan.sh" > >(tee "${SONAR_LOG}") 2>&1 || sonar_exit=$?
  if grep -q '^SonarScanner: SUCCESS$' "${SONAR_LOG}"; then
    scanner_result="success"
  else
    scanner_result="failed"
  fi
  if grep -q '^Quality Gate: PASSED$' "${SONAR_LOG}"; then
    quality_gate="PASSED"
  elif grep -q '^Quality Gate: FAILED$' "${SONAR_LOG}"; then
    quality_gate="FAILED"
  else
    quality_gate="UNAVAILABLE"
  fi
fi

overall_status="passed"
if [[ "${coverage_exit}" -ne 0 \
   || "${tests_total}" -eq 0 \
   || "${failed_tests}" -ne 0 \
   || "${sonar_exit}" -ne 0 \
   || "${quality_gate}" != "PASSED" ]]; then
  overall_status="failed"
fi

cat > "${RESULT_FILE}" <<EOF2
# QA Results

Generated timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Project: sbm-api
Overall status: ${overall_status}

## Tests and coverage

Test exit code: ${coverage_exit}
Collected tests: ${tests_total}
Passed tests: ${passed_tests}
Failed tests: ${failed_tests}
Coverage result: ${coverage_result}
Coverage artifact: coverage.xml

## SonarQube

SonarScanner exit code: ${sonar_exit}
Scanner execution result: ${scanner_result}
Server-side Quality Gate result: ${quality_gate}

## Evidence

QA execution command: ./scripts/qa-check.sh
Runtime: Docker
Django system check: included in scripts/coverage.sh
EOF2

echo "Evidencia QA generada en: context/qa-results.md"

[[ "${overall_status}" == "passed" ]] || exit 1
echo "QA SBM-API completado correctamente."
