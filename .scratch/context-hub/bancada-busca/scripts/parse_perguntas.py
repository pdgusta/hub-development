import re,json,sys
src=r"C:\Projetos\context-hub\.scratch\context-hub\bancada-busca\perguntas.md"
out=[]
for l in open(src,encoding='utf-8'):
    m=re.match(r'\|\s*(\d+)\s*(?:✱)?\s*\|\s*([LP])\s*\|\s*(pt|en)\s*\|(.*)\|(.*)\|\s*$',l)
    if m:
        files=re.findall(r'`([^`]+)`',m.group(5))
        out.append(dict(n=int(m.group(1)),tipo=m.group(2),lang=m.group(3),q=m.group(4).strip(),files=files))
json.dump(out,open(r"C:\Projetos\bancada-busca\perguntas.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
