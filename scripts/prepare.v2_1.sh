#!/bin/bash

cd $(dirname $0)/..

orig=data/v2_1
prep=data-prep/v2_1

src=mr
tgt=lx

mkdir -p $prep

for split in train dev test; do
  echo "preparing $split.tsv"
  file=$orig/webnlg_release_v2.1_$split.json
  out=$prep/$split.tsv
  cp /dev/null $out
  total=$(jq '.entries|length' $file)
  for ((i=0,j=1;j<=$total;i++,j++)); do
    echo -ne "$j/$total\r"
    item=$(jq --argjson i $i --arg j $j '.entries[$i]."\($j)"' $file)
    shp=$(echo "$item" | jq '.shape' | sed 's/^"//;s/"$//')
    typ=$(echo "$item" | jq '.shape_type' | sed 's/^"//;s/"$//')
    mr=$(echo "$item" | \
      jq '.modifiedtripleset[]|"\(.subject) __property_start__ \(.property) __property_end__ \(.object)"' | \
      sed 's/^"//;s/"$//' | \
      sed 's/\\"//g' | \
      perl -pe 's/(?<!_)(?<!__property)_(?!_)/ /g' | \
      awk 'BEGIN{ORS=" __triple__ "} y{print s} {s=$0;y=1} END{ORS="";print s}')
    lxs=$(echo "$item" | jq '.lexicalisations[]."lex"' | sed 's/^"//;s/"$//' | sed 's/\\"//g')
    num_lxs=$(echo "$lxs" | wc -l)
    paste \
      <(echo "$j"  | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$typ"  | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$shp"  | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$mr" | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$lxs") \
      >> $out
  done
done

for split in train dev; do
  echo "preparing $split.shuf.tsv"
  inp=$prep/$split.tsv
  out=$prep/$split.shuf.tsv
  shuf $inp > $out
done

echo "preparing train.$src and train.$tgt"
awk -F '\t' '{print $4}' $prep/train.shuf.tsv > $prep/train.$src
awk -F '\t' '{print $5}' $prep/train.shuf.tsv > $prep/train.$tgt
echo "preparing valid.$src and valid.$tgt"
awk -F '\t' '{print $4}' $prep/dev.shuf.tsv   > $prep/valid.$src
awk -F '\t' '{print $5}' $prep/dev.shuf.tsv   > $prep/valid.$tgt
echo "preparing test.$src and test.$tgt"
awk -F '\t' '{print $1}' $prep/test.tsv  > $prep/test.id
awk -F '\t' '{print $4}' $prep/test.tsv  > $prep/test.$src
awk -F '\t' '{print $5}' $prep/test.tsv  > $prep/test.$tgt

tokenizer=mosesdecoder/scripts/tokenizer/tokenizer.perl
for split in train valid test; do
  echo "preparing $split.tok.$src and $split.tok.$tgt"
  for lang in $src $tgt; do
    inp=$prep/$split.$lang
    out=$prep/$split.tok.$lang
    perl $tokenizer -threads 8 -l en -protected <(echo "\b__\S+__\b") < $inp > $out
  done
done

echo "fairseq-proprecessing"
fairseq-preprocess \
  --source-lang $src --target-lang $tgt \
  --trainpref $prep/train.tok --validpref $prep/valid.tok --testpref $prep/test.tok \
  --destdir $prep \
  --dataset-impl raw

echo "preparing test.uniq.$src-$tgt.$src and test.mref.$src-$tgt.$tgt"
paste $prep/test.id $prep/test.$src-$tgt.$src | \
  awk -F '\t' '!id[$1]++{print $2}' \
  > $prep/test.uniq.$src-$tgt.$src
paste $prep/test.id $prep/test.$src-$tgt.$tgt | \
  awk -F '\t' '{if(NR>1&&$1!=id){printf "\n";} id=$1; print $2}' \
  > $prep/test.mref.$src-$tgt.$tgt