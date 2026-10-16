"""Analise: arquivos que o OHS nao indexou (frontmatter YAML invalido), perguntas afetadas, falhas comuns,
e geracao do resultados.json consolidado."""
import json,re,glob,os
B=r"C:\Projetos\bancada-busca"
log=open(B+r"\logs\ohs-local-index.log",encoding='utf-8').read()
bad=sorted(set(b.replace(chr(92),'/') for b in re.findall(r'corpus\\([^:\n ]+?\.md):',log)))
print(len(bad),bad)
Q=json.load(open(B+r"\perguntas.json",encoding='utf-8'))
print('perguntas com arquivo esperado nao indexado no OHS',[q['n'] for q in Q if any(f in bad for f in q['files'])])
cfgs=['ohs-local-fulltext','ohs-local-hybrid','ohs-local-semantic','mm-bm25','mm-e5']
R={c:json.load(open(B+rf"\resultados\{c}.json",encoding='utf-8')) for c in cfgs}
todas=[q['n'] for q in Q if all(R[c]['perguntas'][q['n']-1]['rank'] is None for c in cfgs)]
print('todas erraram',todas)
for n in todas:
    q=Q[n-1]; print(n,q['tipo'],q['q'],q['files'])
    for c in ('ohs-local-hybrid','mm-e5'): print('  ',c,R[c]['perguntas'][n-1]['top5'][:3])
out={'observacao':'top 5 (arquivos distintos, caminhos relativos ao corpus) por pergunta e configuracao; rank = posicao do 1o arquivo certo ou null',
     'configuracoes_nao_medidas':{'ohs-gateway-embeddinggemma-300m':'429 cota Cloudflare esgotada','ohs-gateway-bge-m3':'429 cota Cloudflare esgotada','mm-gateway-embeddinggemma-300m':'429','mm-gateway-bge-m3':'429'},
     'metricas':{c:R[c]['metricas'] for c in cfgs},
     'rajada':{t:json.load(open(B+rf"\resultados\{t}.json")) for t in ('rajada-ohs','rajada-mm-1a-rodada','rajada-mm-2a-rodada')},
     'perguntas':{c:[{k:r[k] for k in ('n','tipo','lang','top5','rank')} for r in R[c]['perguntas']] for c in cfgs}}
json.dump(out,open(r"C:\Projetos\context-hub\.scratch\context-hub\bancada-busca\resultados.json",'w',encoding='utf-8'),ensure_ascii=False,indent=1)
