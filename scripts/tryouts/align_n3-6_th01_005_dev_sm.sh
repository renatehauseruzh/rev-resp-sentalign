#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


alignment=$base/alignment

data=$base/data

dev=$data/dev_sm

mkdir -p $dev


# create the sentence split tsv file
echo "Start splitting of sentences"
python3 $alignment/split_sentences.py $data/trip_hotels_dev_sm.csv $dev/test_sent_split_dev_sm.tsv
echo "Splitting sentences complete"

# ngram order 3:
echo "Create alignments for ngram order 3, thresholds 0.1 and 0.5"

# create aligned file with ngram order 3 and threshold 0.1
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng3_th01_dev_sm.tsv --ngram-order 3 --threshold 0.1

# create aligned file with ngram order 3 and threshold 0.05
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng3_th005_dev_sm.tsv --ngram-order 3 --threshold 0.05


# ngram order 4:
echo "Create alignments for ngram order 4, thresholds 0.1 and 0.5"

# create aligned file with ngram order 4 and threshold 0.1
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng4_th01_dev_sm.tsv --ngram-order 4 --threshold 0.1

# create aligned file with ngram order 4 and threshold 0.05
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng4_th005_dev_sm.tsv --ngram-order 4 --threshold 0.05


# ngram order 5:
echo "Create alignments for ngram order 5, thresholds 0.1 and 0.5"

# create aligned file with ngram order 5 and threshold 0.1
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng5_th01_dev_sm.tsv --ngram-order 5 --threshold 0.1

# create aligned file with ngram order 6 and threshold 0.05
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng5_th005_dev_sm.tsv --ngram-order 5 --threshold 0.05


# ngram order 6:
echo "Create alignments for ngram order 6, thresholds 0.1 and 0.5"

# create aligned file with ngram order 6 and threshold 0.1
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng6_th01_dev_sm.tsv --ngram-order 6 --threshold 0.1

# create aligned file with ngram order 6 and threshold 0.05
python3 $alignment/align_v2.py $data/tryout/test_sent_split_dev_sm.tsv $dev/ng6_th005_dev_sm.tsv --ngram-order 6 --threshold 0.05