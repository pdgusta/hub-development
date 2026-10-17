#!/bin/sh
# Ticket 36: roda os testes com o git fora do PATH (o montar.mjs falha depois de a pasta nascer) e TEMP isolado;
# conta as pastas hub-ensaio-* que sobram. Uso: sh falha-forcada-36.sh <worktree> <arquivo>...
WT="$1"; shift
B="$TEMP/f36"; rm -rf "$B"; mkdir -p "$B"
NODEDIR=$(dirname "$(command -v node)")
cd "$WT" || exit 1
for f in "$@"; do
  n=$(basename "$f" .test.mjs); T="$B/$n"; mkdir -p "$T"
  TEMP="$T" TMP="$T" PATH="$NODEDIR" node --test "$f" > "$B/$n.log" 2>&1
  echo "$n sai=$? $(grep -E '^ℹ (pass|fail)' "$B/$n.log" | tr '\n' ' ') sobra=$(ls "$T" | tr '\n' ' ')"
done
