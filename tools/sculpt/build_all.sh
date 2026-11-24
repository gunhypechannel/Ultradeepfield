#!/bin/bash
# Rebuild every sculpted Continuum hull into docs/art/rwar/m/ : build_all.sh <workdir>
set -e; W=${1:-/tmp/sculpt}; T=$(cd "$(dirname "$0")"; pwd); D=$T/../../docs/art/rwar/m; mkdir -p $W $D
for row in "cnint cnt_int.py .03 10000" "cncor cnt_cor.py .025 10000" "cnexe cnt_exe.py .03 18000" "cnasm cnt_asm.py .028 14000" "cnfab cnt_fab.py .035 22000" \
           "cneter cnt_eter.py .03 20000" "cndre cnt_dre.py .035 30000" "cncom cnt_com.py .035 30000" "cnrel cnt_rel.py .04 35000" "cnprime cnt_prime.py .055 40000" "cnark cnt_ark.py .045 50000"; do
  set -- $row; python3 $T/$2 $W/$1 $3 >/dev/null; node $T/pack.js $W/$1 $4 $D/$1.bin .03 | sed "s|.*bin|$1|"
done
