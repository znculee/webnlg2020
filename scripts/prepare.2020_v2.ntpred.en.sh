#!/bin/bash

cd $(dirname $0)/..

orig=data-prep/2020_v2_en
prep=data-prep/2020_v2_en.ntpred
src=mr
tgt=lx

mkdir -p $prep

tokenizer=mosesdecoder/scripts/tokenizer/tokenizer.perl
for split in train valid; do
  for lang in $src $tgt; do
    inp=$orig/$split.$lang
    out=$prep/$split.tok.$lang
    perl $tokenizer -threads 8 -l en -protected <(echo "\b__\S+__\b") -no-escape < $inp > $out
  done
done
perl $tokenizer -threads 8 -l en -protected <(echo "\b__\S+__\b") -no-escape < $orig/test.$src > $prep/test.tok.$src
cat \
  <(paste $prep/train.tok.$src $prep/train.tok.$tgt) \
  <(paste $prep/valid.tok.$src $prep/valid.tok.$tgt) | \
  awk -F '\t' '{printf "%s ||| %s\n", $1, $2}' \
  > $prep/corpus
fast_align=fast_align/build/fast_align
atools=fast_align/build/atools
$fast_align -i $prep/corpus -v -d -o -N -r > $prep/align.rev

python scripts/add_ntpred_to_lex.py \
  --input-corpus $prep/corpus \
  --input-align $prep/align.rev \
  --output-nonterminals $prep/nonterminals.txt \
  --output-target $prep/corpus.ntpred.$tgt

num_train=$(wc -l $prep/train.tok.$src | awk '{print$1}')
cat $prep/corpus.ntpred.$tgt | \
  awk \
    -v path="$prep//" \
    -v n="$num_train" \
    -v lang="$tgt" \
    '{print > ((NR<=n) ? (path "train.tok.ntpred." lang) : (path "valid.tok.ntpred." lang))}'

detokenizer=mosesdecoder/scripts/tokenizer/detokenizer.perl
perl $detokenizer -threads 8 -l en < $prep/train.tok.$src > $prep/train.$src
perl $detokenizer -threads 8 -l en < $prep/train.tok.ntpred.$tgt > $prep/train.ntpred.$tgt
perl $detokenizer -threads 8 -l en < $prep/valid.tok.$src > $prep/valid.$src
perl $detokenizer -threads 8 -l en < $prep/valid.tok.ntpred.$tgt > $prep/valid.ntpred.$tgt
perl $detokenizer -threads 8 -l en < $prep/train.tok.$src > $prep/train.$src

cat $orig/indivisible_tokens.txt $prep/nonterminals.txt > $prep/indivisible_tokens.txt

#seenpred=$(grep -Eo '__pred_\S+__' $prep/train.ntpred.$tgt | sort | uniq)
#validpred=$(grep -Eo '__pred_\S+__' $prep/valid.ntpred.$tgt | sort | uniq)
##icdiff <(echo "$seenpred") <(echo "$validpred")
#icdiff  <(echo "$validpred") <(echo "$seenpred")
##echo "$seenpred"
##unseenind
##awk 'NR==FNR{l[$0];next} {for(i=1;i<=NF;i++){if($i ~ /__pred_*/ && $i not in l){unseen=1}} if(unseen){print $0}}' \
##awk 'NR==FNR{l[$0];next} {for(i=1;i<=NF;i++){if(($i ~ /\b__pred_\S+__/) && !($i in l)){print $i}}}' \
  ##<(echo "$seenpred") \
  ##$prep/valid.ntpred.$tgt

  ##<(cat $prep/valid.ntpred.$tgt | perl -pe 's/\b(?!__pred_)\S+//g' | awk '{$1=$1;print}')
