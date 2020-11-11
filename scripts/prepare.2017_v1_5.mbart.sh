#!/bin/bash

cd $(dirname $0)/..

CACHE=cache/fairseq_mbart/mbart.cc25
DATAORIG=data-prep/2017_v1_5
DATAPREP=data-prep/2017_v1_5_mbart
TRAIN=train
VALID=valid
TEST=test
SRC=mr
TGT=lx

mkdir -p ${DATAPREP}

SPM=sentencepiece/build/src/spm_encode
MODEL=${CACHE}/sentence.bpe.model
${SPM} --model=${MODEL} < ${DATAORIG}/${TRAIN}.${SRC} > ${DATAPREP}/${TRAIN}.${SRC}-${TGT}.${SRC}
${SPM} --model=${MODEL} < ${DATAORIG}/${TRAIN}.${TGT} > ${DATAPREP}/${TRAIN}.${SRC}-${TGT}.${TGT}
${SPM} --model=${MODEL} < ${DATAORIG}/${VALID}.${SRC} > ${DATAPREP}/${VALID}.${SRC}-${TGT}.${SRC}
${SPM} --model=${MODEL} < ${DATAORIG}/${VALID}.${TGT} > ${DATAPREP}/${VALID}.${SRC}-${TGT}.${TGT}
${SPM} --model=${MODEL} < ${DATAORIG}/${TEST}.${SRC}  > ${DATAPREP}/${TEST}.${SRC}-${TGT}.${SRC}
${SPM} --model=${MODEL} < ${DATAORIG}/${TEST}.${TGT}  > ${DATAPREP}/${TEST}.${SRC}-${TGT}.${TGT}

cp ${CACHE}/dict.txt ${DATAPREP}/dict.${SRC}.txt
cp ${CACHE}/dict.txt ${DATAPREP}/dict.${TGT}.txt
