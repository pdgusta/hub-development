#!/usr/bin/env bash
# Uma volta da rodada Ralph: o mesmo prompt aos 12, em paralelo; espera todos.
export MSYS_NO_PATHCONV=1
N="$1"
D='C:/Projetos/context-hub/.scratch/construcao-do-hub/planejamento'
mkdir -p "$D/saidas/volta-$N"
P="Volta $N da rodada Ralph de planejamento. Leia e siga $D/PROMPT.md (é o mesmo em toda volta). Esta é a volta $N."
for n in "Worker 1" "Worker 2" "Worker 3" "Worker 4" "Worker 5" "Worker 6" "Worker 7" "Worker 8" "Worker 9" "Worker 10" "Prumo" "Prumo 2"; do
  ( maestri ask "$n" "$P" > "$D/saidas/volta-$N/${n// /-}.txt" 2>&1 ) &
done
wait
echo "volta $N terminou"
grep -c "volta $N " "$D/voltas.md"
grep "volta $N .*mudou o plano: sim" "$D/voltas.md" | wc -l
