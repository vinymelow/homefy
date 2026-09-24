---
name: homefy-browser-research
description: Como o Hermes usa o browser (quando disponível) para pesquisar concorrentes e inspecionar páginas no projeto Homefy — smoke tests controlados, sem scraping em massa, respeito por timeouts, e degradação graciosa para leitura de HTML via curl quando o browser está indisponível na VPS.
---

# Homefy — pesquisa com browser

Instruções operacionais para o Hermes em runs do projeto Homefy (`/root/homefy`). Usar browser apenas quando acrescentar valor sobre ler HTML diretamente.

## 1. Verificar disponibilidade antes de depender do browser

```bash
hermes doctor            # verifica ambiente, pacotes e ferramentas do Hermes
```

- Se o `hermes doctor` reportar a dependência de browser como pendente/ausente, **não instalar nada nem bloquear a tarefa** — anotar a limitação e passar ao modo degradação (secção 4).
- Na VPS a dependência de sistema do browser pode estar pendente; isso é estado conhecido, não erro da tarefa.

## 2. Quando usar o browser

- Inspecionar páginas de concorrentes que exigem JavaScript para renderizar (estrutura real do DOM, não o shell HTML).
- Capturar evidência visual pontual de uma página de referência (hero, bundle selector).
- Smoke tests controlados de páginas próprias (preview do tema, painel).

## 3. Smoke tests controlados (regras de execução)

- Escopo mínimo: visitar apenas as URLs necessárias à tarefa (1–5 páginas típico). Lista de URLs no prompt da task; desvios exigem justificativa no output.
- **Sem scraping em massa:** nada de crawlar lojas concorrentes, ad library em volume ou paginação automática. Extração pontual e manual.
- **Timeouts:** cada navegação com timeout curto (definido pela task; default 30s). Se a página não renderizar no prazo, registar "não renderizável" e seguir com curl/HTML estático — nunca retry em laço.
- **Sem interação:** não fazer login, não submeter formulários, não clicar em CTAs de lojas de terceiros. Leitura apenas.
- Guardar capturas/evidências em `.aiox/external-runs/<run>/artifacts/` quando a task for executada via `workflows/executors/hermes-exec.sh`.

## 4. Degradação graciosa (browser indisponível)

Quando o browser não estiver disponível ou a página falhar:

```bash
curl -sL --max-time 30 -A "Mozilla/5.0" <URL> -o /tmp/page.html
```

- Ler o HTML estático com ferramentas locais (`rg`, `python3` com `html.parser`); é suficiente para copy, preços, meta tags e estrutura de secções server-rendered.
- Se a página for JS-rendered e o HTML vier vazio, registar a limitação no output e pedir ao orquestrador um print/HTML guardado pelo operador — não contornar com automação agressiva.
- Sempre declarar no output qual o modo usado (browser vs curl) e as limitações do resultado.

## Guardrails

- `hermes doctor` antes de assumir browser; degradar para curl, nunca instalar dependências de sistema por conta própria.
- Sem scraping em massa, sem loops de retry, sem interação com sites de terceiros.
- Respeitar timeouts em cada chamada de rede; falha de rede = evidência registada, não exceção fatal.
- Evidências com URL + data (regra do método de pesquisa); nada de fabricar conteúdo de páginas não lidas.
- Nenhuma credencial em URL/comandos; `.env` real nunca é lido para navegação.
