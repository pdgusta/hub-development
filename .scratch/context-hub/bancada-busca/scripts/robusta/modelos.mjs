// Fase 2: catálogo dos modelos de embedding e carregador genérico (transformers.js 4.3.1 ou FreeLLMAPI).
// Prefixos e pooling conforme o model card de cada um (citados em fase2-modelos.md).
import { createRequire } from 'node:module'; import path from 'node:path'; import os from 'node:os';
import { pathToFileURL } from 'node:url';
const BASE = 'C:/Projetos/bancada-busca/robusta';
const require = createRequire(BASE + '/package.json');
const WEB = 'Given a web search query, retrieve relevant passages that answer the query';
// pool: 'graph' = saída sentence_embedding do próprio ONNX; 'mean' | 'cls' | 'last' = sobre last_hidden_state com a máscara.
export const MODELOS = {
  'e5-small': { repo: 'Xenova/multilingual-e5-small', dtype: 'q8', pool: 'mean', q: 'query: ', d: (t) => 'passage: ' + t },
  'granite-97m': { repo: 'ibm-granite/granite-embedding-97m-multilingual-r2', dtype: 'fp32', file: 'model_quint8_avx2', pool: 'cls', q: '', d: t => t },
  'granite-311m': { repo: 'ibm-granite/granite-embedding-311m-multilingual-r2', dtype: 'fp32', file: 'model_quint8_avx2', pool: 'cls', q: '', d: t => t },
  'harrier-270m': { repo: 'onnx-community/harrier-oss-v1-270m-ONNX', dtype: 'q8', pool: 'graph', q: `Instruct: ${WEB}\nQuery: `, d: t => t },
  'embeddinggemma-300m': { repo: 'onnx-community/embeddinggemma-300m-ONNX', dtype: 'q8', pool: 'graph', q: 'task: search result | query: ', d: (t, ti) => `title: ${ti || 'none'} | text: ${t}` },
  'embeddinggemma-2': { repo: 'onnx-community/embeddinggemma-2-ONNX', dtype: 'q8', pool: 'pipeline-mean', q: 'task: search result | query: ', d: (t, ti) => `title: ${ti || 'none'} | text: ${t}` },
  'arctic-m-v2': { repo: 'Snowflake/snowflake-arctic-embed-m-v2.0', dtype: 'q8', pool: 'cls', q: 'query: ', d: t => t },
  'gte-multi-base': { repo: 'onnx-community/gte-multilingual-base', dtype: 'q8', pool: 'cls', q: '', d: t => t },
  'e5-large-instruct': { repo: 'intfloat/multilingual-e5-large-instruct', dtype: 'fp32', sub: 'onnx', ext: true, pool: 'mean', q: `Instruct: ${WEB}\nQuery: `, d: t => t },
  'bge-m3': { repo: 'Xenova/bge-m3', dtype: 'q8', pool: 'cls', q: '', d: t => t },
  'qwen3-0.6b': { repo: 'onnx-community/Qwen3-Embedding-0.6B-ONNX', dtype: 'q8', pool: 'last', q: `Instruct: ${WEB}\nQuery:`, d: t => t },
  'harrier-0.6b': { repo: 'onnx-community/harrier-oss-v1-0.6b-ONNX', dtype: 'q8', pool: 'graph', q: `Instruct: ${WEB}\nQuery: `, d: t => t },
  // API (FreeLLMAPI, /v1/embeddings, nome explícito): o gateway não passa task_type/input_type de consulta.
  'gemini-embedding-001': { api: 'gemini-embedding-001', q: '', d: t => t, lote: 30, pausaMs: 30000 },
  'text-embedding-3-large': { api: 'text-embedding-3-large', q: '', d: t => t, lote: 120, pausaMs: 5000 },
  'embed-v4.0': { api: 'embed-v4.0', q: '', d: t => t, lote: 24, pausaMs: 20000 },
};
export const MAXLEN = 512;

function l2(v) { let n = 0; for (const x of v) n += x * x; n = Math.sqrt(n) || 1; return Float32Array.from(v, x => x / n); }

export async function carregar(slug) {
  const cfg = MODELOS[slug]; if (!cfg) throw new Error('modelo desconhecido ' + slug);
  if (cfg.api) return { cfg, embed: apiEmbedder(cfg) };
  const tf = await import(pathToFileURL(require.resolve('@huggingface/transformers')).href);
  tf.env.cacheDir = path.join(os.homedir(), '.cache', 'huggingface');
  const opts = { dtype: cfg.dtype, ...(cfg.file ? { model_file_name: cfg.file } : {}), ...(cfg.sub ? { subfolder: cfg.sub } : {}), ...(cfg.ext ? { use_external_data_format: true } : {}) };
  if (cfg.pool === 'pipeline-mean') {
    const ex = await tf.pipeline('feature-extraction', cfg.repo, opts);
    return { cfg, embed: async (texts) => (await ex(texts, { pooling: 'mean', normalize: true })).tolist().map(v => Float32Array.from(v)) };
  }
  const tok = await tf.AutoTokenizer.from_pretrained(cfg.repo, cfg.sub ? { subfolder: cfg.sub } : {});
  const model = await tf.AutoModel.from_pretrained(cfg.repo, opts);
  const embed = async (texts) => {
    const inp = tok(texts, { padding: true, truncation: true, max_length: MAXLEN });
    const out = await model(inp);
    const h = out.last_hidden_state ?? out.token_embeddings;
    if (cfg.pool === 'graph' || !h) { if (!out.sentence_embedding) throw new Error('saídas: ' + Object.keys(out)); return out.sentence_embedding.tolist().map(l2); } const [B, T, H] = h.dims; const d = h.data; const m = inp.attention_mask.data;
    const res = [];
    for (let b = 0; b < B; b++) {
      const v = new Float32Array(H);
      if (cfg.pool === 'cls') { for (let k = 0; k < H; k++) v[k] = d[(b * T) * H + k]; }
      else if (cfg.pool === 'last') { let last = -1; for (let t = 0; t < T; t++) if (m[b * T + t]) last = t; for (let k = 0; k < H; k++) v[k] = d[(b * T + last) * H + k]; }
      else { let c = 0; for (let t = 0; t < T; t++) if (m[b * T + t]) { c++; for (let k = 0; k < H; k++) v[k] += d[(b * T + t) * H + k]; } for (let k = 0; k < H; k++) v[k] /= c || 1; }
      res.push(l2(v));
    }
    return res;
  };
  return { cfg, embed };
}

// ---------- FreeLLMAPI
export const API_USO = { chamadas: 0, entradas: 0, tokens_aprox: 0, erros: [] };
function apiEmbedder(cfg) {
  const KEY = process.env.FREELLM_API_KEY; const URL = process.env.FREELLM_URL || 'http://localhost:3001/v1/embeddings';
  if (!KEY) throw new Error('FREELLM_API_KEY ausente');
  return async (texts) => {
    API_USO.chamadas++; API_USO.entradas += texts.length; API_USO.tokens_aprox += Math.round(texts.join('').length / 4);
    const r = await fetch(URL, { method: 'POST', headers: { Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: cfg.api, input: texts }) });
    if (!r.ok) { const e = new Error(`HTTP ${r.status}: ${(await r.text()).slice(0, 300)}`); e.status = r.status; API_USO.erros.push(e.message); throw e; }
    const j = await r.json();
    return j.data.sort((a, b) => a.index - b.index).map(x => l2(x.embedding));
  };
}
