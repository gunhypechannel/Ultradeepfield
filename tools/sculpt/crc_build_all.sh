#!/bin/bash
# v751 rebuild every Carcinid sculpt: tools/sculpt/crc_build_all.sh <workdir> [keys...]  (~4 min on 2 cores) -> docs/art/carcinid/m/<k>.bin
cd "$(dirname "$0")"; W=${1:?workdir}; shift; mkdir -p "$W"
CRABS="cscut cspit charv cguard cbrood cwar ccrys clanc cmolt cmar cmat ctyr cora ckor cbeh ckbr cpal ccrown ccrownm"; SHIPS="cfrig cint cdest cvang ccarr cpearl cmint cregent cempr cbrlord ckrak"
for k in ${@:-$CRABS $SHIPS}; do echo $k; done | xargs -P 2 -I{} sh -c 'k={}; case " '"$CRABS"' " in *" $k "*) py=crc_crab.py; n=24000; e=.06;; *) py=crc_ship.py; n=18000; e=.03;; esac
  python3 $py $k '"$W"'/$k .035 >/dev/null && node pack.js '"$W"'/$k $n ../../docs/art/carcinid/m/$k.bin $e'
