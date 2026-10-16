import json,os,sys
tag=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 20
f=json.load(open("fila.json",encoding="utf-8"))
o={e['slug'] for e in json.load(open("fila-osmose.json",encoding="utf-8"))}
pend=[e for e in f if e['slug'] not in o and not os.path.exists(f"respostas/{e['slug']}.json")]
take=pend[:n*5]
os.makedirs("_lotes_salina",exist_ok=True)
for i in range(0,len(take),5):
    k=i//5+1
    open(f"_lotes_salina/{tag}_{k:02d}.txt","w",encoding="utf-8").write("\n".join(f"{e['chave']} -> {e['slug']}" for e in take[i:i+5])+"\n")
print("pendentes",len(pend),"nesta leva",len(take),"lotes",(len(take)+4)//5)
