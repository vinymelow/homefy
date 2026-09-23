# Setup das Integrações no VPS

Guia de configuração do `ecom-stack` num VPS com Ubuntu 22.04/24.04. Executar na ordem — cada passo depende do anterior.

## Ordem de prioridade

1. **Shopify** — necessário para publicar landing pages (Fase 2 do projeto)
2. **Criativos** — não precisa de API key: geração de imagem local + Pillow
3. **Meta Marketing API** — adiar até escalar além de ~€50/dia (o Ads Manager manual é mais rápido no início)
4. **TikTok Marketing API** — idem

---

## Passo 0 — Trazer o projeto para o VPS

```bash
# opção B (recomendada): subir a pasta local para o VPS — IP_DO_VPS é o endereço do teu VPS
scp -r ./ecom-stack usuario@IP_DO_VPS:/home/usuario/
ssh usuario@IP_DO_VPS && cd ~/ecom-stack

# opção A (só para versionamento/backup remoto): requer repo privado no GitHub
# — SEU_USUARIO é o teu username do GitHub, e precisas de chave SSH configurada
# git clone git@github.com:SEU_USUARIO/ecom-stack.git && cd ecom-stack
```

## Passo 1 — Dependências do sistema

```bash
sudo apt update && sudo apt install -y python3 python3-pip nodejs npm git
# Node do Ubuntu é antigo; o Shopify CLI precisa de Node >= 18 (ideal 20 LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v   # deve mostrar v20.x
```

## Passo 2 — Shopify (a única integração obrigatória agora)

### 2.1 — Criar o app na loja

1. Shopify Admin → **Settings → Apps and channels → Develop apps** → **Create an app**
2. Nome: `ecom-stack`
3. **Configuration → Admin API integration** → marcar os scopes:

- `read_products`, `write_products`
- `read_themes`, `write_themes`
- `read_content`, `write_content`
- `read_orders` (para métricas de kill/scale)
- `read_inventory`, `read_shipping` (opcional, para claims de stock/envio)

4. **API credentials → Install app** → copiar o **Admin API access token** (só aparece completo uma vez)

### 2.2 — Gravar no `.env`

```bash
cp config/config.example.env config/.env
nano config/.env
```

```ini
SHOPIFY_STORE_DOMAIN=seu-loja.myshopify.com
SHOPIFY_ADMIN_API_TOKEN=shpat_xxxxxxxxxxxxxxxx
chmod 600 config/.env   # token nunca vai para o git
```

> `.env` já está no `.gitignore`. Nunca commitar.

### 2.3 — Testar (pelo CLI do projeto ou direto)

```bash
python3 cli/cli.py status
# deve mostrar: .env configurado: sim

# teste direto à API (não precisa de instalar o Shopify CLI):
set -a; . ./config/.env; set +a
curl -s "https://$SHOPIFY_STORE_DOMAIN/admin/api/2025-07/themes.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ADMIN_API_TOKEN" | head -c 300
# resposta JSON com os temas = integração OK
```

### 2.4 — (Opcional) Shopify CLI para edição de temas

```bash
npm install -g @shopify/cli
shopify theme list --store=seu-loja.myshopify.com
# abre o browser para autenticar; depois lista os temas da loja
```

Regra permanente: o tema **MAIN é read-only** — duplicar antes de qualquer escrita (`shopify theme push --unpublished` ou duplicar no Admin).

## Passo 3 — Meta Marketing API (quando escalar)

1. [developers.facebook.com](https://developers.facebook.com) → **My Apps → Create App** → tipo *Business*
2. Adicionar o produto **Marketing API**
3. Em **Business Manager**: anotar **Ad Account ID** (`act_123...`) e **Pixel ID**
4. Token: em *Tools → Graph API Explorer* gerar token com permissões `ads_management` + `ads_read`; para produção, criar um **System User** no Business Manager com token permanente
5. Gravar no `.env`:

```ini
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
META_AD_ACCOUNT_ID=act_123456789
META_PIXEL_ID=
```

Teste:

```bash
curl -s "https://graph.facebook.com/v21.0/me/adaccounts?access_token=$META_ACCESS_TOKEN" | head -c 300
```

> **Recomendação:** com €20–50/dia, rodar campanhas manualmente no Ads Manager nas Fases 1–2. A API serve para automação (criar/desligar campanhas por CPA, regras de kill automático) quando houver volume.

## Passo 4 — TikTok Marketing API (quando escalar)

1. [developers.tiktok.com](https://developers.tiktok.com) → **Create App** → tipo *Marketing API* (o acesso à Marketing API exige aprovação do TikTok; pedir cedo, leva dias)
2. OAuth: o app pede autorização da conta de anúncio; guardar `access_token`, `refresh_token`, `advertiser_id`
3. Gravar no `.env`:

```ini
TIKTOK_APP_ID=
TIKTOK_APP_SECRET=
TIKTOK_ACCESS_TOKEN=
TIKTOK_REFRESH_TOKEN=
TIKTOK_ADVERTISER_ID=
```

## Passo 5 — PicsArt

A API oficial (`api.picsart.io`) é enterprise — exige contrato comercial, não serve para dropshipping solo. O pipeline de criativos do projeto **não depende dela**:

- imagens hiper-realistas → plugin local de geração de imagem (5 chaves hiper-realistas)
- cutout do produto → fotos reais + rembg
- overlays de texto → Pillow
- variações de anúncio estático → clone por zonas + QC

Deixar `PICSART_API_KEY=` vazio no `.env` (campo reservado para o futuro).

## Checklist final

```bash
python3 cli/cli.py status
```

| Integração | Status mínimo para a Fase 1 |
| --- | --- |
| Shopify (Admin API) | obrigatória — landing pages dependem dela |
| Criativos | sem chave — sempre disponível |
| Meta | adiar — Ads Manager manual |
| TikTok | adiar — Ads Manager manual |
| PicsArt | dispensada |