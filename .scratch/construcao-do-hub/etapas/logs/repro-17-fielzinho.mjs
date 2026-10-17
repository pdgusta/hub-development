import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { pastaDeEnsaio } from 'file:///C:/context-hub-wt/ticket-17/agents/code/test/pasta-de-ensaio.mjs';
import { gravarItem, tirarItem } from 'file:///C:/context-hub-wt/ticket-17/agents/code/bin/lib/vigia.mjs';
const tela = 'C:/context-hub-wt/ticket-17/agents/code/hooks/vigia/tela.mjs';
test('sonda: estado de outros hooks sem passada não prova sincronização', () => {
  const hub = pastaDeEnsaio('hub-ensaio-17-fielzinho-');
  gravarItem(hub, { id: 'acervo-peca-sumida', nivel: 'informa', resumo: 'peça sumida' });
  tirarItem(hub, 'acervo-peca-sumida');
  const estado = JSON.parse(fs.readFileSync(path.join(hub, '.local/vigia/estado.json'), 'utf8'));
  assert.equal(estado.passada, undefined);
  console.log('estado produzido pela biblioteca:', JSON.stringify(estado));
  for (const modo of ['inicio', 'barra']) {
    const r = spawnSync(process.execPath, [tela, modo, 'claude', '--hub', hub], {
      input: JSON.stringify({ cwd: hub }), encoding: 'utf8',
      env: { ...process.env, HUB_MCP_BANCO_LEITURA_URL: '', HUB_MCP_BANCO_LEITURA_TOKEN: '' },
    });
    assert.equal(r.status, 0);
    console.log(modo + ':', r.stdout);
    assert.match(r.stdout, /em ordem/); // confirma o defeito, não o comportamento desejado
  }
});
