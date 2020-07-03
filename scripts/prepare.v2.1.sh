#!/bin/bash

cd $(dirname $0)/..

orig=data/v2.1
prep=data-prep/v2.1

mkdir -p $prep

for split in train dev test; do
  echo "preparing $split..."
  file=$orig/webnlg_release_v2.1_$split.json
  out_mr=$prep/$split.mr-lx.mr
  out_lx=$prep/$split.mr-lx.lx
  cp /dev/null $out_mr
  cp /dev/null $out_lx
  total=$(jq '.entries' $file | jq 'length')
  for ((i=0,j=1;j<=$total;i++,j++)); do
    echo -ne "$j/$total\r"
    item=$(jq '.entries' $file | jq --argjson i $i --arg j $j '.[$i]."\($j)"')
    mr=$(echo "$item" | jq '.modifiedtripleset' | \
      jq '.[]|"\(.object) __property_start__ \(.property) __property_end__ \(.subject)"' | \
      sed 's/^"//;s/"$//' | \
      awk 'BEGIN{ORS=" __triple__ "} y{print s} {s=$0;y=1} END{ORS="";print s}')
    lxs=$(echo "$item" | jq '.lexicalisations' | jq '.[]."lex"' | sed 's/^"//;s/"$//')
    num_lxs=$(echo "$lxs" | wc -l)
    mrs=$(echo "$mr" | awk -v n=$num_lxs '{for(i=0;i<n;i++)print}')
    echo "$mrs" >> $out_mr
    echo "$lxs" >> $out_lx
  done
done
