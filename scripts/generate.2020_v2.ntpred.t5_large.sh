#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
data=2020_v2_en.ntpred
model=t5_large
SAVEDIR=checkpoints/$data.$model
testpfx=valid
hyp=$SAVEDIR/hyp.$testpfx.txt
src=data-prep/$data/$testpfx.mr
ref=data-prep/$data/$testpfx.lx

#python finetune-transformers/generate.py \
  #--model-class "t5" \
  #--output-path $(readlink -f $hyp) \
  #--test-source-data-path $(readlink -f $src) \
  #--save-dir $(readlink -f $SAVEDIR) \
  #--batch-size 8 \
  #--beam-size 5 \
  #--max-length 200 \
  #--clean-up-tokenization-spaces

# for analysis only
python scripts/compute_ntpred_treeacc.py \
  --source $(readlink -f $src) \
  --target $(readlink -f $hyp) \
  --output-path $(readlink -f $SAVEDIR/valid.score)

#python scripts/compute_ntpred_treeacc.py \
  #--source $(readlink -f $src) \
  #--target $(readlink -f $hyp)

#rmntpred () {
  #sed 's/__pred_\S\+//g' | awk '{$1=$1;print}'
#}

#hyprmntpred=$SAVEDIR/hyp.$testpfx.rmntpred.txt
#cat $hyp | rmntpred > $hyprmntpred
#python e2e-metrics/measure_scores.py -p $ref $hyprmntpred 2> /dev/null
