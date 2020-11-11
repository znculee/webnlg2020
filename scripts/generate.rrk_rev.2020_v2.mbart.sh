#!/bin/bash

cd $(dirname $0)/..

export CUDA_VISIBLE_DEVICES=0
TMPDIR=/tmp
data=2020_v2_ru
model=mbart
SAVEDIR=checkpoints/$data.$model
testpfx=test
gen=gen.$testpfx.rrk_rev.txt
hyp=hyp.$testpfx.rrk_rev.txt
src=data-prep/$data/$testpfx.en_XX
ref=data-prep/$data/$testpfx.ru_RU
beam_size=5

tmp=$SAVEDIR/tmp
mkdir -p $tmp

CACHE=cache/fairseq_mbart/mbart.cc25
langs=ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN

# generating
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
  --beam $beam_size --nbest $beam_size \
  > $tmp/gen.txt

beam_repeat () {
  awk -v n="$beam_size" '{for(i=0;i<n;i++)print}'
}

# preparing for rescoring
cat $src | beam_repeat > $tmp/src
grep ^H- $tmp/gen.txt | awk -F '\t' '{print $3}' > $tmp/hyp
ln -s $(readlink -f $tmp/hyp) $tmp/test.lx-mr.lx
ln -s $(readlink -f $tmp/src) $tmp/test.lx-mr.mr
REVMDLDATA=data-prep/2020_v2_ru.rev
ln -s $(readlink -f $REVMDLDATA/dict.lx.txt) $tmp/dict.lx.txt
ln -s $(readlink -f $REVMDLDATA/dict.mr.txt) $tmp/dict.mr.txt

# rescoring
REVMDLDIR=checkpoints/$data.rev.$model
fairseq-generate data-prep/$data \
  --gen-subset $testpfx \
  --path $REVMDLDIR/checkpoint_best.pt \
  --task translation_from_pretrained_bart \
  --source-lang ru_RU --target-lang en_XX \
  --bpe 'sentencepiece' --sentencepiece-model $CACHE/sentence.bpe.model \
  --max-sentences 16 \
  --langs $langs \
  --dataset-impl raw \
  --score-reference | \
  grep ^H- | sort -n -k 2 -t - | \
  awk -F '\t' '{print $2}' \
  > $tmp/score

# reranking
paste \
  <(sed 's/^/-/;s/^--//' $tmp/score) \
  <(grep ^S- $tmp/gen.txt | beam_repeat) \
  <(grep ^T- $tmp/gen.txt | beam_repeat) \
  <(grep ^H- $tmp/gen.txt) \
  <(grep ^P- $tmp/gen.txt) | \
  awk -v n="$beam_size" 'BEGIN{OFS="\t"}{print int((NR-1)/n),$0}' | \
  sort -n -k 1,1 -k 2,2 | \
  awk -v n="$beam_size" 'NR%n==1 {print}' | \
  awk -F '\t' '{printf"%s\t%s\n%s\t%s\n%s\t%s\t%s\n%s\t%s\n",$3,$4,$5,$6,$7,$8,$9,$10,$11}' \
  > $SAVEDIR/$gen

rm -rf $tmp

grep ^H- $SAVEDIR/$gen | sort -n -k 2 -t - | awk -F '\t' '{print $3}' > $SAVEDIR/$hyp
#python e2e-metrics/measure_scores.py -p $ref $SAVEDIR/$hyp 2> /dev/null
