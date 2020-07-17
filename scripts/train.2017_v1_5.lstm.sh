#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=2017_v1_5
model=lstm
SAVEDIR=checkpoints/$data.$model

mkdir -p $SAVEDIR

fairseq-train data-prep/$data \
  --task translation --arch $model \
  --max-epoch 500 --patience 20 \
  --optimizer adam --lr 1e-3 --clip-norm 0.1 \
  --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
  --max-sentences 128 \
  --dropout 0.2 \
  --encoder-embed-dim 300 --decoder-embed-dim 300 \
  --encoder-hidden-size 128 --decoder-hidden-size 128 \
  --encoder-layers 1 --decoder-layers 1 \
  --dataset-impl raw \
  --save-dir $SAVEDIR \
  --no-epoch-checkpoints \
  | tee $SAVEDIR/log.txt
