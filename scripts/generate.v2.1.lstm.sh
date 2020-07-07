#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=v2.1
model=lstm
SAVEDIR=checkpoints/$data.$model
testpfx=test
gen=gen.txt

fairseq-generate data-prep/$data \
  --gen-subset $testpfx \
  --path $SAVEDIR/checkpoint_best.pt \
  --dataset-impl raw \
  --max-sentences 128 \
  --beam 5 \
  --max-len-a 2 --max-len-b 200 \
  > $SAVEDIR/$gen

bash scripts/measure_scores.sh $SAVEDIR/$gen data-prep/$data/$testpfx.mr-lx.lx
