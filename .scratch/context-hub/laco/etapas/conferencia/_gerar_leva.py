import json,os,sys
leva=int(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 20
f=json.load(open("fila.json",encoding="utf-8"))
pend=[e for e in f if not os.path.exists(f"respostas/{e['slug']}.json")]
take=list(reversed(pend))[:n*5]
os.makedirs("_lotes_tear",exist_ok=True)
for i in range(0,len(take),5):
    k=i//5+1
    open(f"_lotes_tear/L{leva:02d}_{k:02d}.txt","w",encoding="utf-8").write("\n".join(f"{e['chave']} -> {e['slug']}" for e in take[i:i+5])+"\n")
print("pendentes",len(pend),"nesta leva",len(take),"lotes",(len(take)+4)//5)
