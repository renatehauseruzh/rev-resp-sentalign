#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..

alignment=$base/alignment

data=$base/data

dev=$data/dev

mkdir -p $dev

# create the empty gold standard tsv file
# python3 $scripts/create_gs_file.py $data/trip_hotels_test_1000_rand.csv $data/goldstandard_v1.tsv

python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng4_th005_dev_sm.tsv --ngram-order 4 --threshold 0.05
