import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import {spawnSync} from 'node:child_process';
const raiz=fs.mkdtempSync(path.join(os.tmpdir(),'hub-ensaio-22-fielzinho-'));
try {
  const env=path.join(raiz,'cliente.env'), contrato=path.join(raiz,'contrato.md');
  fs.writeFileSync(env,'HUB_PROXY_URL=http://127.0.0.1:8790\n'); fs.writeFileSync(contrato,'# Contrato sintético\n');
  const ambiente={...process.env,CLAUDE_CONFIG_DIR:path.join(raiz,'claude'),CODEX_HOME:path.join(raiz,'codex'),COPILOT_HOME:path.join(raiz,'copilot')};
  const ligar=()=>{const r=spawnSync('pwsh',['-NoProfile','-File','C:/context-hub-wt/ticket-22/agents/code/kit/cliente/ligar-cliente.ps1','-EnvFile',env,'-Contrato',contrato],{env:ambiente,encoding:'utf8'}); if(r.status!==0) throw new Error(r.stdout+r.stderr);};
  ligar(); const toml=path.join(ambiente.CODEX_HOME,'config.toml');
  fs.writeFileSync(toml,fs.readFileSync(toml,'utf8').replace('# hub-cliente:fim','[projects.ensaio]\ntrust_level = "trusted"\n# hub-cliente:fim'));
  console.log('tabela_alheia_antes='+fs.readFileSync(toml,'utf8').includes('[projects.ensaio]'));
  ligar(); console.log('tabela_alheia_depois='+fs.readFileSync(toml,'utf8').includes('[projects.ensaio]'));
} finally { if(path.dirname(raiz)!==os.tmpdir()||!path.basename(raiz).startsWith('hub-ensaio-22-fielzinho-'))throw new Error('fora'); fs.rmSync(raiz,{recursive:true,force:true}); }
