#!/bin/bash

if [ $# -eq 2 ]; then
  gen=$(readlink -f $1)
  ref=$(readlink -f $2)
else
  echo "Usage: measure_scores hypothesis reference"
  exit 0
fi

cd $(dirname $0)/..

SCORER=e2e-metrics/measure_scores.py
tmp=scripts/tmp
hyp=$tmp/hyp
mkdir -p $tmp

grep ^H- $gen | sort -n -k 2 -t - | awk -F '\t' '{print $3}' > $hyp
python $SCORER -p $ref $hyp 2> /dev/null

rm -rf $tmp
