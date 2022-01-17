#! /bin/bash

scripts=`dirname "$0"`
base=$scripts/..


alignment=$base/alignment

data=$base/data

evaluation=$data/evaluation/sentTransformer

mkdir -p $evaluation



echo "Create alignments with paraphrase model"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th01.json --threshold 0.1 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th02.json --threshold 0.2 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th03.json --threshold 0.3 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th04.json --threshold 0.4 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th05.json --threshold 0.5 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_para_th06.json --threshold 0.6 --scoring "sentence embedding" --model "sentence-transformers/paraphrase-MiniLM-L3-v2"



echo "Create alignments with nli model"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th01.json --threshold 0.1 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th02.json --threshold 0.2 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th03.json --threshold 0.3 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th04.json --threshold 0.4 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th05.json --threshold 0.5 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"

python3 $alignment/align.py $data/goldstandard/rev-resp-goldstandard_empty_115.csv $evaluation/st_nli_th06.json --threshold 0.6 --scoring "sentence embedding" --model "sentence-transformers/nli-mpnet-base-v2"