#!/usr/bin/env bash
# Cria os 11 recrutas da construção (Worker 1..10 e Prumo 2; o Prumo já existe) e liga os 12 entre si.
# Rodar pelo Gustavo: ! bash C:/Projetos/context-hub/.scratch/construcao-do-hub/recrutar.sh
export MSYS_NO_PATHCONV=1
CMD='claude --model claude-opus-5-5 --effort high --permission-mode auto'
DIR='C:\Projetos\context-hub'
NOMES=()
for i in 1 2 3 4 5 6 7 8 9 10; do NOMES+=("Worker $i"); done
NOMES+=("Prumo 2")
for n in "${NOMES[@]}"; do
  maestri recruit "$n" --command "$CMD" --dir "$DIR" 2>&1 | tail -1
done
TODOS=("${NOMES[@]}" "Prumo")
for ((a=0; a<${#TODOS[@]}; a++)); do
  for ((b=a+1; b<${#TODOS[@]}; b++)); do
    maestri connect "${TODOS[a]}" "${TODOS[b]}" >/dev/null 2>&1 || echo "falhou: ${TODOS[a]} <-> ${TODOS[b]}"
  done
done
echo "pronto: ${#TODOS[@]} recrutas ligados entre si"
