#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
data=2017_v1_5
model=t5_large
SAVEDIR=checkpoints/$data.$model
testpfx=test
hyp=$SAVEDIR/hyp.$testpfx.rrk_orac.txt
src=data-prep/$data/$testpfx.uniq.mr-lx.mr
ref=data-prep/$data/$testpfx.mref.mr-lx.lx
beam_size=5

tmp=$SAVEDIR/tmp
mkdir -p $tmp

# generating
python finetune-transformers/generate.py \
  --model-class "t5" \
  --output-path $(readlink -f $tmp/hyp) \
  --test-source-data-path $(readlink -f $src) \
  --save-dir $(readlink -f $SAVEDIR) \
  --batch-size 16 \
  --beam-size $beam_size \
  --num-return-sequences $beam_size \
  --max-length 200

beam_repeat () {
  awk -v n="$beam_size" '{for(i=0;i<n;i++)print}'
}

# rescoring
python scripts/scorer.bleu.mref.py \
  --output-path $(readlink -f $tmp/score) \
  --beam-size $beam_size \
  --hyp $(readlink -f $tmp/hyp) \
  --ref $(readlink -f $ref)

# reranking
paste $tmp/score $tmp/hyp | \
  awk -v n="$beam_size" 'BEGIN{OFS="\t"}{print int((NR-1)/n),$0}' | \
  sort -n -k 1,1 -k 2,2 | \
  awk -v n="$beam_size" 'NR%n==0 {print}' | \
  awk -F '\t' '{print $3}' \
  > $hyp

rm -rf $tmp

python e2e-metrics/measure_scores.py -p $ref $hyp 2> /dev/null
