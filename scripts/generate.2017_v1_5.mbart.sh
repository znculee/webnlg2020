#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=2017_v1_5_mbart
model=mbart
SAVEDIR=checkpoints/$data.$model
testpfx=test
gen=gen.$testpfx.txt

CACHE=cache/fairseq_mbart/mbart.cc25
langs=ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN

fairseq-generate data-prep/$data \
  --gen-subset $testpfx \
  --path $SAVEDIR/checkpoint_best.pt \
  --task translation_from_pretrained_bart \
  -s mr -t lx \
  --bpe 'sentencepiece' --sentencepiece-model $CACHE/sentence.bpe.model \
  --scoring sacrebleu \
  --remove-bpe 'sentencepiece' \
  --max-sentences 32 \
  --langs $langs \
  --dataset-impl raw \
  --beam 5 \
  > $SAVEDIR/$gen

#bash scripts/measure_scores.sh $SAVEDIR/$gen data-prep/$data/$testpfx.mref.mr-lx.lx
