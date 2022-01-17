#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


alignment=$base/alignment

data=$base/data

ngram=$data/evaluation/ngram

sentt=$data/evaluation/sentTransformer

goldstandard=$data/goldstandard

results=$data/results

mkdir -p $results



echo "Evaluate alignments for ngram orders 4-6, thresholds 0.02 - 0.16"

python3 $alignment/evaluate.py \
--gs_file $goldstandard/rev-resp-goldstandard_annotated_115.json \
--outfile $results/ng4-6_th002-016.csv \
--hyp_files $ngram/ng4_th002.json \
$ngram/ng4_th004.json \
$ngram/ng4_th006.json \
$ngram/ng4_th008.json \
$ngram/ng4_th01.json \
$ngram/ng4_th012.json \
$ngram/ng4_th014.json \
$ngram/ng4_th016.json \
$ngram/ng5_th002.json \
$ngram/ng5_th004.json \
$ngram/ng5_th006.json \
$ngram/ng5_th008.json \
$ngram/ng5_th01.json \
$ngram/ng5_th012.json \
$ngram/ng5_th014.json \
$ngram/ng5_th016.json \
$ngram/ng6_th002.json \
$ngram/ng6_th004.json \
$ngram/ng6_th006.json \
$ngram/ng6_th008.json \
$ngram/ng6_th01.json \
$ngram/ng6_th012.json \
$ngram/ng6_th014.json \
$ngram/ng6_th016.json


# senttransformer paraphrase model
echo "Evaluate alignments of paraphrase model, thresholds 0.1 - 0.6"

python3 $alignment/evaluate.py \
--gs_file $goldstandard/rev-resp-goldstandard_annotated_115.json \
--outfile $results/st_th01-06_paraphrase.csv \
--hyp_files $sentt/st_para_th01.json \
$sentt/st_para_th02.json \
$sentt/st_para_th03.json  \
$sentt/st_para_th04.json \
$sentt/st_para_th05.json \
$sentt/st_para_th06.json


# senttransformer nli model
echo "Evaluate alignments of NLI model, thresholds 0.1 - 0.6"

python3 $alignment/evaluate.py \
--gs_file $goldstandard/rev-resp-goldstandard_annotated_115.json \
--outfile $results/st_th01-06_nli.csv \
--hyp_files $sentt/st_nli_th01.json \
$sentt/st_nli_th02.json \
$sentt/st_nli_th03.json  \
$sentt/st_nli_th04.json \
$sentt/st_nli_th05.json \
$sentt/st_nli_th06.json
