#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
data=2020_v2_en
model=t5_large
SAVEDIR=checkpoints/$data.$model
testpfx=valid
hyp=$SAVEDIR/hyp.$testpfx.rrk_rev_chrf.txt
src=data-prep/$data/$testpfx.mr
ref=data-prep/$data/$testpfx.lx
beam_size=5

tmp=$SAVEDIR/tmp
mkdir -p $tmp

## generating
#python finetune-transformers/generate.py \
  #--model-class "t5" \
  #--output-path $(readlink -f $tmp/hyp) \
  #--test-source-data-path $(readlink -f $src) \
  #--save-dir $(readlink -f $SAVEDIR) \
  #--batch-size 16 \
  #--beam-size $beam_size \
  #--num-return-sequences $beam_size \
  #--max-length 200

beam_repeat () {
  awk -v n="$beam_size" '{for(i=0;i<n;i++)print}'
}

## rescoring
#REVMDLDIR=checkpoints/$data.$model.rev
#cat $src | beam_repeat > $tmp/src
#python finetune-transformers/generate.py \
  #--model-class "t5" \
  #--output-path $(readlink -f $tmp/hyp_of_src) \
  #--test-source-data-path $(readlink -f $tmp/hyp) \
  #--save-dir $(readlink -f $REVMDLDIR) \
  #--batch-size 16 \
  #--beam-size $beam_size \
  #--max-length 200

python chrF/chrF++.py -R $tmp/src -H $tmp/hyp_of_src -s | \
  tail -n +2 | head -n -3 | awk '{print$2}' \
  > $tmp/score

# reranking
paste $tmp/score $tmp/hyp | \
  awk -v n="$beam_size" 'BEGIN{OFS="\t"}{print int((NR-1)/n),$0}' | \
  sort -n -k 1,1 -k 2,2 | \
  awk -v n="$beam_size" 'NR%n==0 {print}' | \
  awk -F '\t' '{print $3}' \
  > $hyp

#rm -rf $tmp

python e2e-metrics/measure_scores.py -p $ref $hyp 2> /dev/null
