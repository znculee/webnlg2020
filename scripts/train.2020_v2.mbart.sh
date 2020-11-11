#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=2020_v2_ru
model=mbart
SAVEDIR=checkpoints/$data.$model

mkdir -p $SAVEDIR

PRETRAIN=cache/fairseq_mbart/mbart.cc25
langs=ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN

fairseq-train data-prep/$data \
  --encoder-normalize-before --decoder-normalize-before \
  --arch mbart_large --layernorm-embedding \
  --task translation_from_pretrained_bart \
  --source-lang en_XX --target-lang ru_RU \
  --criterion label_smoothed_cross_entropy --label-smoothing 0.2 \
  --max-epoch 500 --patience 20 \
  --optimizer adam --adam-eps 1e-06 --adam-betas '(0.9, 0.98)' \
  --lr-scheduler polynomial_decay --lr 3e-05 --min-lr -1 --warmup-updates 2500 --total-num-update 40000 \
  --dropout 0.3 --attention-dropout 0.1 --weight-decay 0.0 \
  --max-tokens 1024 --update-freq 2 \
  --seed 222 --log-format simple --log-interval 2 \
  --restore-file $PRETRAIN \
  --reset-optimizer --reset-meters --reset-dataloader --reset-lr-scheduler \
  --langs $langs \
  --dataset-impl raw \
  --save-dir $SAVEDIR \
  --no-epoch-checkpoints \
  | tee $SAVEDIR/log.txt
