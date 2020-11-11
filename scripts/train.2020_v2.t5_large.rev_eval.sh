#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
data=2020_v2_en.eval
model=t5_large
SAVEDIR=checkpoints/$data.$model.rev
CACHEDIR=cache/$model

mkdir -p $SAVEDIR
mkdir -p $CACHEDIR

python finetune-transformers/train.py \
  --pretrained-model-path "t5-large" \
  --train-source-data-path $(readlink -f "data-prep/$data/train.lx") \
  --train-target-data-path $(readlink -f "data-prep/$data/train.mr") \
  --valid-source-data-path $(readlink -f "data-prep/$data/valid.lx") \
  --valid-target-data-path $(readlink -f "data-prep/$data/valid.mr") \
  --indivisible-tokens-path $(readlink -f "data-prep/$data/indivisible_tokens.txt") \
  --save-dir $(readlink -f $SAVEDIR) \
  --cache-dir $(readlink -f $CACHEDIR) \
  --max-epoch 500 --patience 10 \
  --batch-size 8 --update-frequency 32 \
  --learning-rate 2e-5 \
  --valid-batch-size 8 \
  #--valid-bleu --valid-beam-size 5 --valid-max-length 200
