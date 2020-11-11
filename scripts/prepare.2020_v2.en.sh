#!/bin/bash

cd $(dirname $0)/..

orig=data/2020_v2/en
prep=data-prep/2020_v2_en

src=mr
tgt=lx

mkdir -p $prep

for split in train dev test; do
  echo "preparing $split.json"
  if [ "$split" == "test" ]; then
    python scripts/xml2json.py --nolex $orig/test $orig/test.json
  else
    python scripts/xml2json.py $orig/$split $orig/$split.json
  fi
done

for split in train dev test; do
  echo "preparing $split.tsv"
  file=$orig/$split.json
  out=$prep/$split.tsv
  cp /dev/null $out
  total=$(jq '.entries|length' $file)
  for ((i=0,j=1;j<=$total;i++,j++)); do
    echo -ne "$j/$total\r"
    item=$(jq --argjson i $i '.entries[$i]' $file)
    category=$(echo "$item" | jq '.["@category"]' | sed 's/^"//;s/"$//')
    mr=$(echo "$item" | \
      jq '.modifiedtripleset.mtriple[]' | \
      sed 's/^"//;s/"$//' | \
      sed 's/\\"//g' | \
      sed 's/_/ /g' | \
      awk -F '|' '{print "__subject__",$1,"__predicate__",$2,"__object__",$3}' | \
      awk '{$1=$1;print}' | \
      awk 'BEGIN{ORS=" "} y{print s} {s=$0;y=1} END{ORS="";print s}')
    if [ "$split" == "test" ]; then
      lxs="placeholder"
      num_lxs=1
    else
      lxs=$(echo "$item" | jq '.lex[]."#text"' | sed 's/^"//;s/"$//' | sed 's/\\"//g')
      num_lxs=$(echo "$lxs" | wc -l)
    fi
    paste \
      <(echo "$j"        | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$category" | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$mr"       | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}') \
      <(echo "$lxs") \
      >> $out
  done
done

awk -F '\t' '{print $2}' $prep/train.tsv | sort | uniq > $prep/category.seen.txt
awk -F '\t' 'NR==FNR{s[$0];next} !($0 in s){print}' \
  $prep/category.seen.txt \
  <(awk -F '\t' '{print $2}' $prep/test.tsv | sort | uniq) \
  > $prep/category.unseen.txt

for split in train dev; do
  echo "preparing $split.shuf.tsv"
  inp=$prep/$split.tsv
  out=$prep/$split.shuf.tsv
  shuf $inp > $out
done

echo "preparing train.$src and train.$tgt"
awk -F '\t' '{print $3}' $prep/train.shuf.tsv > $prep/train.$src
awk -F '\t' '{print $4}' $prep/train.shuf.tsv > $prep/train.$tgt
echo "preparing valid.$src and valid.$tgt"
awk -F '\t' '{print $3}' $prep/dev.shuf.tsv   > $prep/valid.$src
awk -F '\t' '{print $4}' $prep/dev.shuf.tsv   > $prep/valid.$tgt
echo "preparing test.$src and test.$tgt"
awk -F '\t' '{print $1}' $prep/test.tsv  > $prep/test.id
awk -F '\t' '{print $2}' $prep/test.tsv  > $prep/test.cat
awk -F '\t' '{print $3}' $prep/test.tsv  > $prep/test.$src
awk -F '\t' '{print $4}' $prep/test.tsv  > $prep/test.$tgt

echo "preparing test.uniq.$src and test.mref.$tgt"
awk -F '\t' '{if(!id[$1]++) print $2}' \
  <(paste $prep/test.id $prep/test.$src) \
  > $prep/test.uniq.$src
awk -F '\t' '{if($1!=id) printf "\n"; id=$1; print $2}' \
  <(paste $prep/test.id $prep/test.$tgt) | \
  sed '1{/^$/d}' \
  > $prep/test.mref.$tgt

echo "preparing test.seen.uniq.$src and test.seen.mref.$tgt"
awk -F '\t' 'NR==FNR{s[$0];next} {if(!id[$1]++&&($2 in s)) print $3}' \
  $prep/category.seen.txt \
  <(paste $prep/test.id $prep/test.cat $prep/test.$src) \
  > $prep/test.seen.uniq.$src
awk -F '\t' 'NR==FNR{s[$0];next} {if(!($2 in s)) next; if($1!=id) printf "\n"; id=$1; print $3}' \
  $prep/category.seen.txt \
  <(paste $prep/test.id $prep/test.cat $prep/test.$tgt) | \
  sed '1{/^$/d}' \
  > $prep/test.seen.mref.$tgt

echo "preparing test.unseen.uniq.$src and test.unseen.mref.$tgt"
awk -F '\t' 'NR==FNR{s[$0];next} {if(!id[$1]++&&!($2 in s)) print $3}' \
  $prep/category.seen.txt \
  <(paste $prep/test.id $prep/test.cat $prep/test.$src) \
  > $prep/test.unseen.uniq.$src
awk -F '\t' 'NR==FNR{s[$0];next} {if($2 in s) next; if($1!=id) printf "\n"; id=$1; print $3}' \
  $prep/category.seen.txt \
  <(paste $prep/test.id $prep/test.cat $prep/test.$tgt) | \
  sed '1{/^$/d}' \
  > $prep/test.unseen.mref.$tgt

