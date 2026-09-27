# Deploy do cockpit Homefy

O cockpit fica em `https://app.homefyshop.online`. O domínio principal e `www`
continuam sob controle da Shopify.

## DNS Hostinger

Crie somente este registro: `A app 179.198.193.119` (TTL padrão). Não altere
os registros `@` ou `www`.

## Serviços

- `homefy-web.service`: FastAPI em `127.0.0.1:8787`, sem executor embutido.
- `homefy-worker.service`: consome a fila e chama o executor Hermes.
- Traefik: termina HTTPS e encaminha apenas o hostname do subdomínio.

Estado persistente: `/var/lib/homefy`. Logs: `/var/log/homefy`. Segredos:
`/etc/homefy/`, modo `0600`, fora do Git.

Na primeira abertura, use o token de uso único em
`/var/lib/homefy/bootstrap-token`, crie a senha e confirme o TOTP. Depois disso,
o endpoint de criação de conta é desativado permanentemente.

