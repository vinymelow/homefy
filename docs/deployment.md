# Deployment e ambientes

## Estado atual: NENHUM deploy automático

O Homefy **não tem deploy automático**. Nenhum pipeline publica código ou
conteúdo sozinho — nem no repositório, nem em Shopify, Meta ou TikTok. O que
existe:

- **VPS = ambiente de build e teste.** Todo o desenvolvimento, a execução de
  tasks via Hermes e os smoke tests acontecem nesta VPS. Os artefatos de execução
  ficam em `.aiox/external-runs/` (locais, gitignored).
- **Versionamento por Git, com operações manuais.** Commits, pushes e qualquer
  publicação são ações do operador. Regras críticas do `AGENTS.md`: nunca
  commitar segredos; nunca rodar `npx aiox-core install --force` sem avaliar
  conflitos.

## Painel local (acesso via túnel SSH)

O painel web do projeto roda apenas em localhost na VPS — por design. Para
abri-lo remotamente, use um túnel SSH:

```bash
# Na sua máquina local:
ssh -L 8787:127.0.0.1:8787 usuario@IP_DO_VPS
# Na VPS:
python3 ecom-stack/cli/cli.py painel --porta 8787
# No browser local: http://127.0.0.1:8787
```

A CLI (`python3 ecom-stack/cli/cli.py ajuda`) oferece ainda `status`,
`brief novo/listar`, `criativo imagem/video`, `anuncio plano` e `doctor`
(verifica `.env` e testa a ligação à Shopify). Detalhes operacionais em
`ecom-stack/docs/setup-vps.md` e `ecom-stack/docs/guia-uso.md`.

## Shopify e publicação em plataformas (futuro)

Hoje a publicação é manual e segue o guia de uso da ecom-stack (tema duplicado,
edição de templates no admin da Shopify). O fluxo automatizado planejado é:

```
QA PASS (qa-specialist)
   → aprovação humana explícita do operador
   → publish (Shopify / Meta / TikTok)
```

**Não implementado — próxima fase.** O que já está pronto para esse fluxo:
gate de QA com veredito estruturado (`result.json`), regra de autoridade que
proíbe agentes de publicar sozinhos, e variáveis de ambiente para as APIs
(`SHOPIFY_*`, `META_*`, `TIKTOK_*` em `ecom-stack/config/.env`). O que falta:
o passo de `publish` em si — não prometa nem assuma mais que isso.

## Rollback plan (conceitual)

Sem deploy automático, o rollback é majoritariamente **"não aplicar"**:

- **Código/documentação (Git):** branches por mudança; revert/rebase antes do
  merge; histórico completo como última rede de segurança.
- **Artefatos de execução:** runs são imutáveis em
  `.aiox/external-runs/<run>/` — um resultado ruim não sobrescreve o anterior;
  basta ignorá-lo e reexecutar.
- **Tema Shopify (operação manual atual):** a regra de ouro da ecom-stack é
  nunca escrever no tema MAIN — trabalhar sempre num tema duplicado; rollback =
  reativar o tema anterior.
- **Variáveis de ambiente:** `.env` é local e gitignored; versiona-se apenas o
  `config.example.env` (placeholders).

Uma política de rollback automatizado para o futuro fluxo de publish —
**Não implementado — próxima fase**, junto com o próprio publish.
