#!/usr/bin/env node
/**
 * validate-squad.js — valida um squad AIOX usando o validador oficial.
 * Uso: node squads/ecommerce-growth/tools/validate-squad.js [nome-do-squad] [--strict]
 * Default: ecommerce-growth. Exit 0 = PASS, 1 = FAIL.
 */
const path = require('path');

const root = path.resolve(__dirname, '..', '..', '..');
const { SquadValidator } = require(path.join(root, '.aiox-core', 'development', 'scripts', 'squad', 'squad-validator.js'));
const { SquadLoader } = require(path.join(root, '.aiox-core', 'development', 'scripts', 'squad', 'squad-loader.js'));

async function main() {
  const args = process.argv.slice(2).filter(a => a !== '--strict');
  const name = args[0] || 'ecommerce-growth';
  const strict = process.argv.includes('--strict');

  const loader = new SquadLoader({ squadsPath: path.join(root, 'squads') });
  const validator = new SquadValidator({ strict, verbose: true });

  let squadPath;
  try {
    const resolved = await loader.resolve(name);
    squadPath = resolved.path;
  } catch (e) {
    console.error(`Squad não encontrado: ${name} (${e.message})`);
    process.exit(1);
  }

  console.log(`Validando squad: ${name} (${squadPath})${strict ? ' [strict]' : ''}\n`);
  const result = await validator.validate(squadPath);

  const fmt = (r) => {
    const mark = r.valid === false ? '✗ FAIL' : (r.valid ? '✓ PASS' : '⚠ WARN');
    console.log(`  [${mark}] ${r.check || r.name || 'check'}`);
    if (r.errors) r.errors.forEach(e => console.log(`      erro: ${e.message || e}`));
    if (r.warnings) r.warnings.forEach(w => console.log(`      aviso: ${w.message || w}`));
  };

  // Resultado agregado: tenta formatos conhecidos
  if (Array.isArray(result.results)) result.results.forEach(fmt);
  else if (Array.isArray(result.checks)) result.checks.forEach(fmt);

  if (result.details) {
    for (const [k, v] of Object.entries(result.details)) {
      if (v && typeof v === 'object') {
        console.log(`\n${k}:`);
        if (Array.isArray(v.results)) v.results.forEach(fmt);
        else if (Array.isArray(v.checks)) v.checks.forEach(fmt);
        else if (v.errors) { const mark = v.valid === false ? '✗ FAIL' : '✓ PASS'; console.log(`  [${mark}] ${k}`); v.errors.forEach(e => console.log(`      erro: ${e.message || e}`)); }
      }
    }
  }

  console.log(`\n== RESULTADO: ${result.valid === false ? 'FAIL' : 'PASS'} ==`);
  if (result.summary) console.log(JSON.stringify(result.summary, null, 2));
  process.exit(result.valid === false ? 1 : 0);
}

main().catch(e => { console.error('Erro inesperado:', e.message); process.exit(1); });
