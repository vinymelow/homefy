# Integração AIOX → Hermes

O Homefy delega a execução de tasks ao **Hermes Agent v0.20.2** por meio do
executor `workflows/executors/hermes-exec.sh`, que segue o contrato de
executores externos de `.aiox-core/development/external-executors/README.md`:
o orquestrador (AIOX) mantém a autoridade; o executor externo apenas executa a
tentativa delegada e grava artefatos.

- **Hermes:** instalado pelo usuário, fora do repositório — binário em
  `~/.local/bin/hermes` (também disponível para o usuário de sistema `hermes`
  em `/home/hermes/.local/bin/hermes`). O executor escolhe a instalação do
  usuário `hermes` quando ela consegue ler o workdir; senão, a do root.
- **Modelo default:** Groq `llama-3.3-70b-versatile` (provider/modelo em
  `~/.hermes/config.yaml`; override por execução com `-m`).
- **Modo de execução:** one-shot, `hermes -z "<prompt>" --in <workdir> --usage-file <run>/usage.json`.

## Contrato do executor

### Uso

```bash
hermes-exec.sh -t <slug> -f <prompt_file> [-d workdir] [-m model] [-T timeout]
hermes-exec.sh -t <slug> -p "prompt inline" [-d workdir]
```

| Argumento | Obrigatório | Descrição |
|---|---|---|
| `-t` / `--task` | sim | Slug da task (vira `<timestamp>-<slug>` do run) |
| `-f` / `--prompt-file` | sim* | Arquivo de prompt (copiado para o run) |
| `-p` / `--prompt` | sim* | Prompt inline (alternativa a `-f`) |
| `-d` / `--workdir` | não | Diretório de trabalho (default: cwd) |
| `-m` / `--model` | não | Override de modelo do Hermes |
| `-T` / `--timeout` | não | Timeout em minutos (default: 20, alinhado com `modelGovernance.timeouts.defaultMinutes`) |
| `-r` / `--run-dir` | não | Base dos runs (default: `.aiox/external-runs`) |

### Contrato de status

| Status | Condição | Exit code do script |
|---|---|---|
| `SUCCESS` | Exit 0, saída não vazia, sem padrões fatais | 0 |
| `PARTIAL` | Exit 0, mas saída vazia/curta demais — **revisão humana necessária** | 0 |
| `FAILED` | Exit ≠ 0, **ou padrão fatal detectado na saída/log mesmo com exit 0** | 1 |
| `TIMEOUT` | Excedeu o timeout (`-T`; kill via `timeout --signal=TERM`) | 124 |
| `REJECTED` | Pré-checks falharam: workdir ilegível/inexistente, prompt vazio, prompt-file ilegível, Hermes ausente | 65/69 |

**Detecção de erro fatal com exit 0:** o Hermes pode terminar com exit 0 mesmo
em erro fatal (ex.: HTTP 404 de modelo). O executor varre `output.md` e
`hermes.log` pelos padrões `HTTP [45]xx`, `does not exist or you do not have
access`, `Invalid API key`, `Traceback`, `Connection refused`,
`NameResolutionError` e faz downgrade de SUCCESS → FAILED.

### Saída stdout (key=value)

```
STATUS=started|finished|failed|timeout|rejected
RUN_DIR=...        OUTPUT=...        PROMPT=...
COMMAND=...        EXIT_CODE=...     RESULT_JSON=...
```

### Artefatos por run (`.aiox/external-runs/<timestamp>-<slug>/`)

| Arquivo | Conteúdo |
|---|---|
| `prompt.md` | Prompt exato enviado ao Hermes |
| `command.txt` | Comando completo executado (quoted) |
| `output.md` | stdout do Hermes |
| `hermes.log` | stderr do Hermes |
| `usage.json` | Utilização: tokens, `api_calls`, custo estimado, modelo/provider, flags `completed`/`failed` |
| `result.json` | Resultado estruturado (ver abaixo) |
| `metadata.json` | Metadados legados (backward compat) |
| `artifacts/` | Artefatos que o Hermes gravar durante o run |

O diretório `.aiox/external-runs/` é **gitignored** — runs são artefatos
locais; revise-os antes de partilhar (podem conter dados sensíveis da tarefa).

## Como ler `result.json` e `usage.json`

`result.json`:

```json
{
  "run_id": "20260924-091225-e2e-integration-test",
  "task": "e2e-integration-test",
  "status": "FAILED",
  "started_at": "...", "finished_at": "...",
  "exit_code": 0,
  "model": null,
  "workdir": "/root/homefy",
  "artifacts": { "output": "...", "log": "...", "usage": "...", "dir": "..." },
  "output_bytes": 94,
  "usage": { ... }
}
```

- **`status`** é o veredito do run (maiusculizado). Note que `exit_code: 0` com
  `status: FAILED` é possível — a detecção de padrão fatal sobrepõe o exit code.
- **`usage`** espelha o `usage.json` do Hermes: `input_tokens`,
  `output_tokens`, `total_tokens`, `api_calls`, `estimated_cost_usd`,
  `model`, `provider`, `completed`, `failed`. Quando o run falha antes de
  chamar o modelo, os campos de token/custo vêm `null` e `failed: true`.

Exemplo de inspeção rápida:

```bash
RUN=.aiox/external-runs/<timestamp>-<slug>
cat $RUN/result.json | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['status'], r['exit_code'], r['output_bytes'])"
```

## Governança aplicada na execução

- **Timeout:** 20 min default (`-T`), 60 min para long-running, 10 min para
  automação de browser — limites de `modelGovernance.timeouts`.
- **Budget:** teto diário/mensal com `block_and_notify`; o custo por run vem no
  `usage.json` (`estimated_cost_usd`) e o contador acumulado fica em
  `.aiox/usage/budget-counter.json`. Verifique antes de reexecutar em massa.
- **Max iterations:** 25 default / 15 por task, hard stop
  (`hardStopOnExceed`).
- **Fallback de modelo:** ordem primary → cheap, máx. 2 retries
  (`fallback.order`, `maxModelRetries`); routing AIOX (sonnet/opus/haiku) é
  metadado — a execução real usa o provider configurado no Hermes.

## Degradação graciosa

A automação de browser do Hermes depende de componentes de sistema **pendentes
nesta VPS**. Enquanto não são instalados:

- tarefas que precisam de browser devem usar o fallback **HTTP básico via
  `curl`** (fetch de páginas, APIs) ou ser adiadas;
- o restante do runtime (terminal, arquivos, skills, MCP nativo) opera normal;
- `hermes doctor` lista o estado das dependências — trate os itens de browser
  como pendência conhecida, não como regressão.

Skills Hermes: as específicas do projeto fazem staging em `.hermes/skills/`;
o Hermes também tem skills de hub instaladas em `~/.hermes/skills/` (fora do
repo). Configuração de provider/chaves em `~/.hermes/config.yaml` e
`~/.hermes/.env` — nunca no repositório.

## Exemplos

```bash
# Task padrão a partir de arquivo
workflows/executors/hermes-exec.sh -t smoke-test-project-structure \
  -f squads/ecommerce-growth/tasks/smoke-test-project-structure.md \
  -d /root/homefy

# Prompt inline com modelo e timeout customizados
workflows/executors/hermes-exec.sh -t analise-rapida \
  -p "Resume em 5 linhas a estrutura de ecom-stack/" \
  -d /root/homefy -m llama-3.3-70b-versatile -T 10

# Inspeção do resultado
cat .aiox/external-runs/<run>/result.json
```
