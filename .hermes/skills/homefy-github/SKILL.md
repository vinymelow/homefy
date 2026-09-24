---
name: homefy-github
description: Convenções Git do projeto Homefy — trabalhar na branch main com commits organizados, proibição de force push, nunca commitar .env, secret scan obrigatório antes de commit, e push normal apenas após validação.
---

# Homefy — convenções Git

## 1. Estado do repositório

```bash
cd /root/homefy
git status                          # ver estado antes de mexer
git log --oneline -5                # ver o padrão de commits recentes
git branch --show-current           # confirmar a branch (main)
```

- Branch principal: `main`. Trabalho direto na `main` com commits pequenos e organizados (padrão histórico do repo: "sync vps: DD/MM/AAAA HH:MM" para syncs, mensagens descritivas em pt para mudanças de conteúdo).
- Commits atômicos por tema (ex.: "Adiciona skills de domínio research/ecommerce", "Atualiza brief do produto X") — não misturar temas num commit só.

## 2. Secret scan antes de cada commit (obrigatório)

```bash
cd /root/homefy
git add -A
git status --short | awk '{print $2}' | grep -vE '\.env($|\.)|config/\.env' | while read -r f; do
  [ -f "$f" ] && grep -InE 'api[_-]?key|access[_-]?token|secret|password' "$f" || true
done
```

- Regras do scan:
  - Padrões: `api_key`, `apikey`, `api-key`, `access_token`, `access-token`, `secret`, `password` (case-insensitive via `-i`).
  - **Exclusões obrigatórias:** `ecom-stack/config/.env` (`.env` real, gitignored), `config.example.env`, `.env.example`/templates, documentação que descreve as variáveis sem valores, ficheiros em `node_modules/`.
  - Exceções legítimas (nomes de variáveis em código/docs sem valor) têm de ser verificadas uma a uma antes de seguir.
- Qualquer valor real encontrado = **não commitar**; remover o valor, rotacionar a credencial se foi exposta, e repetir o scan.
- O `.env` real nunca sai da máquina: `ecom-stack/config/.env` está gitignored — confirmar com `git status` que não aparece em `git add -A`.

## 3. Commit e push

```bash
git commit -m "mensagem descritiva do tema"
```

- **Push apenas após validação:** o trabalho entregue tem de passar nas verificações do projeto (ex.: `bash -n` em scripts, `python3 ecom-stack/cli/cli.py doctor` quando tocar na loja, checklists aplicáveis) antes do `git push`.
- Push normal (`git push origin main`); **nunca `git push --force`** — histórico publicado não se reescreve.
- Sync automático: o repo tem `sync-github.sh`/`sync-github.log` na raiz do home — se existir um fluxo de sync ativo, respeitar a janela dele e não intercalar pushes manuais com o sync.

## 4. O que nunca fazer

- `git push --force` / `git push -f` (em nenhuma branch).
- Commitar `.env`, `ecom-stack/config/.env`, tokens, chaves de API ou passwords — em ficheiro ou em mensagem de commit.
- Commitar em `squads/` ou `.aiox-core/` fora do escopo da própria task do squad (`.aiox-core/` nunca se edita à mão).
- `git commit --amend` / `git rebase` sobre commits já enviados (pushados).

## Guardrails

- Secret scan sempre antes do commit; qualquer hit real = stop and report.
- Push só depois de validação verde; sem force push, sem rebase de histórico publicado.
- `.env` real permanece local e gitignored; exemplos/templates só com placeholders.
- Em caso de dúvida sobre um valor ser segredo, tratar como segredo.
