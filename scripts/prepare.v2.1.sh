#!/bin/bash

cd $(dirname $0)/..

orig=data/v2.1
prep=data-prep/v2.1

mkdir -p $prep

for split in train dev test; do
  echo "preparing $split..."
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
      jq '.modifiedtripleset[]|"\(.object) __property_start__ \(.property) __property_end__ \(.subject)"' | \
      sed 's/^"//;s/"$//' | \
      sed 's/\\"//g' | \
      perl -pe 's/(?<!_)(?<!__property)_(?!_)/ /g' | \
      awk 'BEGIN{ORS=" __triple__ "} y{print s} {s=$0;y=1} END{ORS="";print s}')
    lxs=$(echo "$item" | jq '.lexicalisations[]."lex"' | sed 's/^"//;s/"$//')
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
