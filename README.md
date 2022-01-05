# rev-resp-sentalign

## Requirements

- The following commands work in a unix-like system with bash
- Python 3 must be installed on your system


## Commands

The following commands are executed from rev-resp-alignment as working directory

### Tryout
To try out some things a very small development dataset containing 100
documents is used (data/trip_hotels_dev_sm.csv)

To produce a set of alignments for ngram orders 3 - 6 with thresholds 0.1 and 0.05 for a first impression, use:

    ./scripts/align_n3-6_th01_005_dev_sm.sh

To try out different settings, first split the sentences with the command

    python3 alignment/split_sentences.py data/trip_hotels_dev_sm.csv data/dev_sm/test_sent_split_dev_sm.tsv

Then the alignments can be done with individual settings with a command such as

    python3 alignment/alig_v2.py data/dev_sm/test_sent_split_dev_sm.tsv data/dev_sm/ng5_th001_dev_sm.tsv --ngram order 5 --threshold 0.01
    
