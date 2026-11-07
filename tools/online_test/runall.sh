#!/bin/bash
cd "$(dirname "$0")"; python3 -m http.server 8123 >/dev/null 2>&1 & SRV=$!; sleep 1
for r in ${RUNS:-"phone1 fresh R1" "fold1 switch R2" "open1 fresh R3"}; do set -- $r; mkdir -p sh$3; rm -f sh$3/*
  DEV=$1 SCEN=$2 SHOTS=sh$3 MAXIT=4000 timeout 6000 node obot.js > $3.log 2>&1; echo "$3 finished"; done
kill $SRV; echo ALLDONE
