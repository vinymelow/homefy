# Segurança

Regras explícitas de segurança do Homefy. Complementam as 5 regras críticas do
`AGENTS.md` (das quais a nº 1 — nunca commitar segredos — é a mais relevante
aqui).

## 1. Segredos

- **Onde ficam.** O `.env` real fica em `ecom-stack/config/.env` (gitignored) e
  as credenciais do Hermes em `~/.hermes/` (`config.yaml`, `.env`) — ambos fora
  do versionamento. `ecom-stack/config/config.example.env` lista as variáveis
  (Shopify, Meta, TikTok, Picsart) com placeholders **vazios** e serve apenas
  como referência para criar o `.env` local.
- **Como criar.** `cp ecom-stack/config/config.example.env ecom-stack/config/.env`
  e preencher localmente. Nunca commitar, nunca copiar para outra máquina sem
  criptografia, nunca colar em chat.
- **Proibições.** Segredos não aparecem em: código, README, documentação,
  prompts, tasks, workflows YAML, templates, logs nem artefatos de run. Em
  qualquer desses lugares, use apenas placeholders (`<TOKEN>`, `SHOPIFY_ADMIN_API_TOKEN=`, …).
- **Varredura antes de commitar** (rode na raiz do repo):

  ```bash
  grep -RInE 'api[_-]?key|access[_-]?token|secret|password|private[_-]?key' . \
    --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.aiox-core \
    --exclude-dir=external-runs --exclude='*.example.env'
  ```

  Investigue qualquer ocorrência antes de commitar. (O `.gitignore` já cobre
  `.env`, `.env.*`, `*.key`, `*.pem`, `logs/` e `.aiox/external-runs/`, mas a
  varredura pega o que o ignore não vê.)

## 2. OAuth tokens e API keys

- **Shopify:** `SHOPIFY_ADMIN_API_TOKEN` (app Custom Admin API; escopo mínimo
  necessário — ver `ecom-stack/docs/setup-vps.md` §2). O token só aparece
  completo uma vez no admin; guarde-o no `.env`, não em outro lugar.
- **Meta:** `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID`.
- **TikTok:** `TIKTOK_ACCESS_TOKEN` + `TIKTOK_ADVERTISER_ID`.
- **GitHub / outros:** chaves como `GITHUB_TOKEN` (usado pelo Hermes para o hub
  de skills) ficam em `~/.hermes/.env`, fora do repo.
- Tokens vazam por logs e prints: ao executar tasks via Hermes, lembre que o
  prompt e a saída ficam gravados em `.aiox/external-runs/<run>/` — não inclua
  segredos em prompts e revise artefatos antes de partilhar.

## 3. Browser sessions e cookies

A automação de browser está pendente nesta VPS. Quando for instalada: sessões,
cookies e storages de browser usados por agentes são tão sensíveis quanto
senhas (dão acesso a contas logadas: Shopify admin, Meta Ads, TikTok). Regras:
manter fora do repo, nunca versionar perfis de browser, invalidar sessões após
uso e não reutilizar cookies entre ambientes.

## 4. SSH

- Acesso à VPS por chave SSH (sem senha em texto claro); o uso de agente de
  chaves (`ssh-add`) é recomendado em vez de chaves soltas em disco.
- Chaves privadas (`id_*`, `*.pem`) nunca entram no repo — o `.gitignore`
  cobre `*.pem`/`*.key`, mas o envio acidental deve ser verificado na
  varredura acima.
- O túnel SSH para o painel (`ssh -L 8787:127.0.0.1:8787 …`) mantém o painel
  em localhost-only por design — não exponha a porta publicamente.

## 5. Logs e artefatos

- `.aiox/external-runs/` é gitignored e contém prompt, comando, saída e log de
  cada run: trate como dado sensível. **Revise antes de partilhar** — a saída
  de uma task pode conter dados do produto, URLs internas ou trechos de
  credenciais se o prompt foi mal construído.
- `hermes.log` (`logs/` em geral) também é gitignored; não redirecione logs
  para fora dessas pastas.
- A task `smoke-test-project-structure` exemplifica a regra: o agente deve
  **avisar** se encontrar um `.env` preenchido, sem jamais revelar valores.

## 6. Claims de e-commerce (integridade, não só sigilo)

- **Nunca inventar** preços, descontos, garantias, prazos de envio, stock ou
  prova social em páginas, criativos ou copy — tudo deriva do Product Brief
  aprovado (ver `docs/agents.md`).
- Claims sem evidência são reprovados no gate de QA e, fora do sistema,
  constituem risco legal/publicitário para a loja.

## 7. Responsabilidade final

- **O operador humano aprova publicações.** Deploy/publicação em Shopify, Meta
  e TikTok só ocorre com confirmação explícita (regra crítica 5 do `AGENTS.md`).
  Nenhum agente, workflow ou executor tem permissão de publicar.
- Falhas de segurança (token exposto, `.env` commitado, sessão vazada) seguem o
  mesmo caminho de qualquer falha crítica: **halt_and_escalate** — parar o
  fluxo, revogar o segredo afetado e corrigir antes de continuar.
