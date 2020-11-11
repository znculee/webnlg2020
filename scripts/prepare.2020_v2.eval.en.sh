#!/bin/bash

# Combine train and valid for training a overfitting reverse model to do a
# better content based evaluation

cd $(dirname $0)/..

orig=data-prep/2020_v2_en
prep=data-prep/2020_v2_en.eval

mkdir -p $prep

cat $orig/train.mr $orig/valid.mr > $prep/train.mr
cat $orig/train.lx $orig/valid.lx > $prep/train.lx

ln -s $(readlink -f $orig/valid.mr) $prep/valid.mr
ln -s $(readlink -f $orig/valid.lx) $prep/valid.lx
ln -s $(readlink -f $orig/test.mr) $prep/test.mr
ln -s $(readlink -f $orig/indivisible_tokens.txt) $prep/indivisible_tokens.txt
