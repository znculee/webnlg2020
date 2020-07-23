#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=v2_1
model=transformer
SAVEDIR=checkpoints/$data.$model

mkdir -p $SAVEDIR

fairseq-train data-prep/$data \
  --task translation --arch $model \
  --max-epoch 500 --patience 20 \
  --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
  --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --dropout 0.3 --weight-decay 0.0001 \
  --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
  --max-tokens 4096 \
  --dataset-impl raw \
  --save-dir $SAVEDIR \
  --no-epoch-checkpoints \
  | tee $SAVEDIR/log.txt

