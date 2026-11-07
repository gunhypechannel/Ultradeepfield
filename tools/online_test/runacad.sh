#!/bin/bash
cd "$(dirname "$0")"; python3 -m http.server 8123 >/dev/null 2>&1 & SRV=$!; sleep 1
rm -f shF/* shS/*
DEV=phone1 SCEN=fresh SHOTS=shF MAXIT=4000 timeout 6000 node obot.js > F1.log 2>&1 &
wait %2; DEV=phone1 SCEN=switch SHOTS=shS MAXIT=4000 timeout 6000 node obot.js > S1.log 2>&1 &
wait %3; kill $SRV; echo ALLDONE
