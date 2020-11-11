#!/bin/bash

cd $(dirname $0)/..

orig=data-prep/2020_v2_ru
prep=data-prep/2020_v2_ru.rev

src=ru_RU
tgt=en_XX

mkdir -p $prep

for ins in $orig/*.$tgt-$src.*; do
  out=$(basename $ins | awk 'BEGIN{FS=".";OFS="."}{$(NF-1)="ru_RU-en_XX";print}')
  cp $ins $prep/$out
done

cp $orig/dict.$src.txt $prep/dict.$src.txt
cp $orig/dict.$tgt.txt $prep/dict.$tgt.txt
