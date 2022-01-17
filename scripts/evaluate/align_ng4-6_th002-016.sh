#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


alignment=$base/alignment

data=$base/data

evaluation=$data/evaluation/ngram

mkdir -p $evaluation

# ngram order 4:

echo "Create alignments for ngram order 4, thresholds 0.02 - 0.16"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th002_lower.json --ngram-order 4 --threshold 0.02 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th004_lower.json --ngram-order 4 --threshold 0.04 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th006_lower.json --ngram-order 4 --threshold 0.06 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th008_lower.json --ngram-order 4 --threshold 0.08 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th01_lower.json --ngram-order 4 --threshold 0.1 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th012_lower.json --ngram-order 4 --threshold 0.12 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th014_lower.json --ngram-order 4 --threshold 0.14 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng4_th016_lower.json --ngram-order 4 --threshold 0.16 --lowercase


# ngram order 5:
echo "Create alignments for ngram order 5, thresholds 0.02 - 0.16"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th002_lower.json --ngram-order 5 --threshold 0.02 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th004_lower.json --ngram-order 5 --threshold 0.04 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th006_lower.json --ngram-order 5 --threshold 0.06 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th008_lower.json --ngram-order 5 --threshold 0.08 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th01_lower.json --ngram-order 5 --threshold 0.1 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th012_lower.json --ngram-order 5 --threshold 0.12 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th014_lower.json --ngram-order 5 --threshold 0.14 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng5_th016_lower.json --ngram-order 5 --threshold 0.16 --lowercase

# ngram order 6:
echo "Create alignments for ngram order 6, thresholds 0.02 - 0.16"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th002_lower.json --ngram-order 6 --threshold 0.02 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th004_lower.json --ngram-order 6 --threshold 0.04 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th006_lower.json --ngram-order 6 --threshold 0.06 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th008_lower.json --ngram-order 6 --threshold 0.08 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th01_lower.json --ngram-order 6 --threshold 0.1 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th012_lower.json --ngram-order 6 --threshold 0.12 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th014_lower.json --ngram-order 6 --threshold 0.14 --lowercase

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/ng6_th016_lower.json --ngram-order 6 --threshold 0.16 --lowercase