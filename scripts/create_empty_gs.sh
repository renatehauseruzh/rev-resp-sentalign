#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..

data=$base/data

mkdir -p $data

# create the empty gold standard tsv file
python3 $scripts/create_gs_file.py $data/trip_hotels_test_1000_rand.csv $data/goldstandard_v1.tsv
