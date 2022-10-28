#!/usr/bin/env python
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import os
import json
import argparse
from tqdm import tqdm
from preprocess import extract_ast
from transformers import PLBartTokenizer

def load_data(args):
    tokenizer = PLBartTokenizer.from_pretrained("uclanlp/plbart-java-cs", src_lang="java", tgt_lang="cs")
    data = []
    with open(args.src_file, 'r', encoding='utf-8') as f1, \
            open(args.tgt_file, 'r', encoding='utf-8') as f2:
        for src, tgt in zip(f1, f2):
            src_extracted = extract_ast(src.strip(), args.src_lang, tokenizer)
            tgt_extracted = ' '.join(tokenizer.tokenize(tgt.strip()))
            data.append({'src': src_extracted, 'tgt': tgt_extracted})
    return data

def process(args):
    processed_dataset = load_data(args)
    
    out_src = os.path.join(args.output_dir, '{}.spm.{}'.format(args.pref, args.src_lang))
    out_tgt = os.path.join(args.output_dir, '{}.spm.{}'.format(args.pref, args.tgt_lang))
    with open(out_src, 'w', encoding='utf-8') as src_writer, \
            open(out_tgt, 'w', encoding='utf-8') as tgt_writer:
        for ex in processed_dataset:
            if ex is not None:
                src_writer.write(ex['src'] + '\n')
                tgt_writer.write(ex['tgt'] + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-file",
        help='path to *.model file',
    )
    parser.add_argument(
        "--src_file",
        type=str,
        default=['-'],
        help="input files (.jsonl) to filter/encode",
    )
    parser.add_argument(
        "--tgt_file",
        type=str,
        default=['-'],
        help="input files (.jsonl) to filter/encode",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=['_'],
        help="path of the output directory",
    )
    parser.add_argument(
        "--src_lang",
        type=str,
        default=['_'],
        help="name of the source language",
    )
    parser.add_argument(
        "--tgt_lang",
        type=str,
        default=['_'],
        help="name of the target language",
    )
    parser.add_argument(
        "--pref",
        type=str,
        default=['_'],
        help="file prefix",
    )
    parser.add_argument(
        "--keep-empty",
        action="store_true",
        help="keep empty lines",
    )
    parser.add_argument("--max_len", type=int, default=510)
    parser.add_argument("--workers", type=int, default=60)
    args = parser.parse_args()
    process(args)


if __name__ == "__main__":
    main()
