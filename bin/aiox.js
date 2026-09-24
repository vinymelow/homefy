#!/usr/bin/env node

/**
 * AIOX CLI wrapper — Homefy
 * Entrypoint executável para o CLI instalado em .aiox-core/cli.
 * O pacote npm aiox-core@5.4.1 não instala bin/ localmente; este wrapper
 * apenas invoca run() exportado por cli/index.js (sem alterar o framework).
 */

const path = require('path');

const cli = require(path.join(__dirname, '..', '.aiox-core', 'cli', 'index.js'));

cli.run(process.argv).catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
