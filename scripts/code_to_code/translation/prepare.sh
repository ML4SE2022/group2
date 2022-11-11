#!/usr/bin/env bash

CURRENT_DIR=$(pwd)
HOME_DIR=$(realpath ../../..)
DATA_DIR=${HOME_DIR}/data/codeXglue/code-to-code/dataset
SPM_DIR=${HOME_DIR}/sentencepiece
SOURCE=$1
TARGET=$2

function spm_preprocess() {

    for SPLIT in train valid test; do
        if [[ $SPLIT == 'test' ]]; then
            MAX_LEN=9999 # we do not truncate test sequences
        else
            MAX_LEN=510
        fi
        python encode.py \
            --model-file ${SPM_DIR}/sentencepiece.bpe.model \
            --src_file $DATA_DIR/${SPLIT}.java-cs.txt.$SOURCE \
            --tgt_file $DATA_DIR/${SPLIT}.java-cs.txt.$TARGET \
            --output_dir $DATA_DIR \
            --src_lang $SOURCE \
            --tgt_lang $TARGET \
            --pref $SPLIT \
            --max_len $MAX_LEN \
            --workers 60
    done

}

function binarize() {

    fairseq-preprocess \
        --source-lang $SOURCE \
        --target-lang $TARGET \
        --trainpref $DATA_DIR/train.spm \
        --validpref $DATA_DIR/valid.spm \
        --testpref $DATA_DIR/test.spm \
        --destdir $DATA_DIR/data-bin \
        --thresholdtgt 0 \
        --thresholdsrc 0 \
        --workers 60 \
        --srcdict ${SPM_DIR}/dict.txt \
        --tgtdict ${SPM_DIR}/dict.txt

    cd ../../../data/codeXglue/code-to-code/dataset/data-bin
    echo '@! 100' >> dict.cs.txt
    echo '@! 100' >> dict.java.txt
}

spm_preprocess
binarize
