"""Gera 200 .md com marcador unico em C:\Projetos\bancada-busca\rajada-src (fora do corpus)."""
import os,glob,shutil
B="C:/Projetos/bancada-busca"
src=sorted(glob.glob(B+"/corpus/issues/*.md"))
dst=B+"/rajada-src"; shutil.rmtree(dst,ignore_errors=True); os.makedirs(dst)
for i in range(1,201):
    t=open(src[i%len(src)],encoding='utf-8').read()
    # corta o frontmatter e limita a tamanho tipico
    t=t[:6000]
    open(f"{dst}/rajada-{i:04d}.md","w",encoding='utf-8').write(f"# Nota de rajada {i}\n\nMarcador unico: marcadorrajada{i:04d}\n\n"+t)
print(len(os.listdir(dst)))
