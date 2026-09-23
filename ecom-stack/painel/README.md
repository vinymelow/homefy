# Painel web do ecom-stack

Interface que concentra o projeto: registas o produto (único trabalho manual),
disparas as etapas do pipeline e acompanhas tudo num só sítio.

## Arrancar

```bash
python3 cli/cli.py painel            # http://127.0.0.1:8787 (só localhost)
python3 cli/cli.py painel --porta 9000
```

Do teu PC abres um túnel SSH e usas no browser:

```bash
ssh -L 8787:localhost:8787 root@IP_DA_VPS
# → http://localhost:8787
```

## O que faz (Fase 1 — MVP)

| Rota | Função |
|---|---|
| `/` | Dashboard: produtos, trabalhos recentes, próximo passo |
| `/novo` | Formulário = as 9 secções do `templates/product-brief.md`; grava em `research/landers/<slug>-brief.md` (formato exato do template — `cli.py` e prompts continuam a funcionar sobre o ficheiro) |
| `/p/<slug>` | Ficha do produto: brief + botões do pipeline + histórico de jobs |
| `/trabalho/<id>` | Log do job com chaves mascaradas |
| `/ativos` | Galeria de `assets/creatives/` e `assets/uploads/` |

### Etapas do pipeline

- **Gerar página de vendas** — job-agente: corre `kimi -p` headless no repo, seguindo
  `prompts/pagina-vendas.md` + o brief. Resultado em `templates/<slug>.html`. Sem custo extra de API.
- **Gerar vídeo 9:16 (Higgsfield)** — job-API direta: Seedance 2.0 (~$0.10/s).
  Requer `HF_API_KEY_ID` + `HF_API_KEY_SECRET` no `config/.env`; sem chaves, falha
  com mensagem clara. Picsart entra na Fase 2 no mesmo slot.

Jobs correm num worker com fila SQLite (`dados/painel.db`) — sobrevive a quedas
(jobs interrompidos voltam à fila ao reiniciar). Logs em `logs/trabalhos/<id>.log`.

## Instalação (já feita nesta VPS)

```bash
sudo apt install -y python3-pip python3-venv
python3 -m venv painel/.venv
painel/.venv/bin/pip install -r painel/requirements.txt
```

## Segurança

- Só escuta em `127.0.0.1`. Para expor publicamente: `PAINEL_TOKEN=<secreto>`
  no ambiente (auth por token) **e** HTTPS (ex.: Caddy) — sem ambos, não expor.
- O `.env` é lido apenas server-side; logs mascaram `*_TOKEN`/`*_KEY*`.

## Roadmap

- **Fase 2**: etapas-agente de imagem (galeria PDP EcomAlchemist, hiper-realistas,
  clone de ad estático), publicação Shopify (duplicar tema antes de escrever — nunca no MAIN),
  Picsart como alternativa de geração, contact sheet de QC.
- **Fase 3**: Meta/TikTok — publicar anúncios e métricas de kill/scale.

## Testado

Subida de servidor, criação de produto via formulário, job-agente end-to-end
(página gerada em `templates/escova-alisadora.html` com placeholders respeitados),
caminho de erro do vídeo sem chaves, compatibilidade com `cli.py brief listar/status`.
