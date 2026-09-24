#!/usr/bin/env bash
# run-smoke-test.sh — smoke test oficial do squad ecommerce-growth (Homefy)
#
# Executa a cadeia AIOX → task → Hermes → resultado de forma não destrutiva:
# roda a task smoke-test-project-structure.md via ponte hermes-exec.sh, imprime
# o result.json do run e valida o contrato de status.
#
# Uso:
#   bash squads/ecommerce-growth/scripts/run-smoke-test.sh
#   (pode ser corrido a partir de qualquer diretório — o script auto-localiza
#   a raiz do repositório; parâmetros fixos conforme contrato do squad)
#
# Contrato:
#   - Executor: workflows/executors/hermes-exec.sh
#     -t smoke-test-$(date +%H%M%S)   slug único por execução
#     -f squads/ecommerce-growth/tasks/smoke-test-project-structure.md
#     -d /root/homefy                 workdir do projeto
#     -T 10                           timeout de 10 minutos
#   - Exit 0 se result.json.status for SUCCESS ou PARTIAL.
#   - Exit 1 para qualquer outro status (FAILED / TIMEOUT / REJECTED) ou se o
#     result.json não for produzido.
#
# Saída: stdout do executor, conteúdo de result.json e veredito final.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
HERMES_EXEC="$ROOT/workflows/executors/hermes-exec.sh"
TASK_FILE="$ROOT/squads/ecommerce-growth/tasks/smoke-test-project-structure.md"
WORKDIR="/root/homefy"
TIMEOUT_MIN=10
SLUG="smoke-test-$(date +%H%M%S)"

if [[ ! -x "$HERMES_EXEC" ]]; then
  echo "ERRO: executor não encontrado ou sem permissão de execução: $HERMES_EXEC" >&2
  exit 1
fi
if [[ ! -r "$TASK_FILE" ]]; then
  echo "ERRO: task não encontrada: $TASK_FILE" >&2
  exit 1
fi

cd "$ROOT"

echo "== run-smoke-test: slug=$SLUG workdir=$WORKDIR timeout=${TIMEOUT_MIN}m =="

# O executor pode sair não-zero (failed=1, timeout=124); capturamos o exit code
# sem abortar o script para conseguirmos inspecionar o result.json.
set +e
EXEC_OUT="$("$HERMES_EXEC" -t "$SLUG" -f "$TASK_FILE" -d "$WORKDIR" -T "$TIMEOUT_MIN")"
EXEC_EXIT=$?
set -e
printf '%s\n' "$EXEC_OUT"
echo "-- executor exit code: $EXEC_EXIT"

RESULT_JSON="$(printf '%s\n' "$EXEC_OUT" | sed -n 's/^RESULT_JSON=//p' | tail -n 1)"
if [[ -z "$RESULT_JSON" || ! -f "$RESULT_JSON" ]]; then
  echo "SMOKE TEST FALHOU: result.json não foi produzido (executor exit=$EXEC_EXIT)" >&2
  exit 1
fi

echo "-- result.json ($RESULT_JSON):"
cat "$RESULT_JSON"
echo

STATUS="$(python3 - "$RESULT_JSON" <<'PY'
import json, sys
try:
    with open(sys.argv[1]) as f:
        print(json.load(f).get("status", ""))
except Exception as e:
    print(f"UNPARSEABLE:{e}")
PY
)"

case "$STATUS" in
  SUCCESS|PARTIAL)
    echo "SMOKE TEST OK: status=$STATUS (executor exit=$EXEC_EXIT)"
    exit 0
    ;;
  *)
    echo "SMOKE TEST FALHOU: status=$STATUS (executor exit=$EXEC_EXIT)" >&2
    exit 1
    ;;
esac
