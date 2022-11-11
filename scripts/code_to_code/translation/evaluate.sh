#!/usr/bin/env bash

export PYTHONIOENCODING=utf-8
CURRENT_DIR=$(pwd)
HOME_DIR=$(realpath ../../..)

declare -A LANG_MAP
LANG_MAP['java']='java'
LANG_MAP['cs']='c_sharp'

while getopts ":h" option; do
    case $option in
    h | *) # display help
        echo
        echo "Syntax: bash run.sh GPU_ID SRC_LANG TGT_LANG"
        echo "SRC_LANG/TGT_LANG  Language choices: [$(
            IFS=\|
            echo "${!LANG_MAP[@]}"
        )]"
        echo
        exit
        ;;
    esac
done

GPU=$1
SOURCE=$2
TARGET=$3

PATH_2_DATA=${HOME_DIR}/data/codeXglue/code-to-code/dataset
CB_EVAL_SCRIPT=${HOME_DIR}/evaluation/CodeBLEU/calc_code_bleu.py

langs=java,cs

SAVE_DIR=${CURRENT_DIR}/${SOURCE}_${TARGET}
USER_DIR=${HOME_DIR}/source

export CUDA_VISIBLE_DEVICES=$GPU

function generate() {

    model=${SAVE_DIR}/checkpoint_best.pt
    FILE_PREF=${SAVE_DIR}/output
    RESULT_FILE=${SAVE_DIR}/result.txt
    GOUND_TRUTH_PATH=$PATH_2_DATA/test.java-cs.txt.${TARGET}

    fairseq-generate $PATH_2_DATA/data-bin \
        --user-dir $USER_DIR \
        --path $model \
        --truncate-source \
        --task translation_without_lang_token \
        --gen-subset test \
        -t $TARGET -s $SOURCE \
        --sacrebleu \
        --remove-bpe 'sentencepiece' \
        --max-len-b 200 \
        --beam 5 \
        --batch-size 4 \
        --langs $langs >$FILE_PREF

    cat $FILE_PREF | grep -P "^H" | sort -V | cut -f 3- | sed 's/\[${TARGET}\]//g' >$FILE_PREF.hyp
    
    echo "CodeXGlue Evaluation" >${RESULT_FILE}
    python ${HOME_DIR}/evaluation/bleu.py \
        --ref $GOUND_TRUTH_PATH \
        --pre $FILE_PREF.hyp \
        2>&1 | tee -a ${RESULT_FILE}

    echo "CodeBLEU Evaluation" >>${RESULT_FILE}
    export PYTHONPATH=${HOME_DIR}
    python $CB_EVAL_SCRIPT \
        --refs $GOUND_TRUTH_PATH \
        --hyp $FILE_PREF.hyp \
        --lang ${LANG_MAP[$TARGET]} \
        2>&1 | tee -a ${RESULT_FILE}

}

generate
