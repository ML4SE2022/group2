#!/usr/bin/env bash

#############################################
#        Download java_cs checkpoint         #
#############################################

FILE=java_cs.zip
# https://drive.google.com/file/d/1ytwgiHFJd4crSVKvwVqWZSyqzfLeN0Bj

if [[ ! -d "java_cs" ]]; then
    fileid="1ytwgiHFJd4crSVKvwVqWZSyqzfLeN0Bj"
    curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" >/dev/null
    curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=$(awk '/download/ {print $NF}' ./cookie)&id=${fileid}" -o ${FILE}
    rm ./cookie
    unzip ${FILE} && rm ${FILE}
fi

# #############################################
# #        Download cs_java checkpoint         #
# #############################################

FILE=cs_java.zip
# https://drive.google.com/file/d/1x1uhNV4ARLvcM6TXv9PiKY5j6pbE2A91

if [[ ! -d "cs_java" ]]; then
    fileid="1x1uhNV4ARLvcM6TXv9PiKY5j6pbE2A91"
    curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" >/dev/null
    curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=$(awk '/download/ {print $NF}' ./cookie)&id=${fileid}" -o ${FILE}
    rm ./cookie
    unzip ${FILE} && rm ${FILE}
fi