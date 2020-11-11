#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=2020_v2_ru
model=mbart
SAVEDIR=checkpoints/$data.$model
testpfx=valid
gen=gen.$testpfx.txt
hyp=hyp.$testpfx.txt
ref=data-prep/$data/$testpfx.ru_RU

CACHE=cache/fairseq_mbart/mbart.cc25
langs=ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN

gen=gen.tmp
fairseq-generate data-prep/$data \
  --gen-subset $testpfx \
  --path $SAVEDIR/checkpoint_best.pt \
  --task translation_from_pretrained_bart \
  --source-lang en_XX --target-lang ru_RU \
  --bpe 'sentencepiece' --sentencepiece-model $CACHE/sentence.bpe.model \
  --scoring sacrebleu \
  --remove-bpe 'sentencepiece' \
  --max-sentences 32 \
  --langs $langs \
  --dataset-impl raw \
  --beam 5 \
  > $SAVEDIR/$gen

#grep ^H- $SAVEDIR/$gen | sort -n -k 2 -t - | awk -F '\t' '{print $3}' > $SAVEDIR/$hyp
#python e2e-metrics/measure_scores.py -p $ref $SAVEDIR/$hyp 2> /dev/null
