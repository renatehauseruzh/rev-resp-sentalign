# rev-resp-sentalign

## Requirements

- The following commands work in a unix-like system with bash
- Python 3 must be installed on your system
- Install the requirements specified in requirements.txt


## Commands

The following commands are executed from rev-resp-alignment as working directory

### Alignment
To align a corpus of review-response pairs, use the following script align.py. There are two options, 
how the similarity should be calculated: an n-gram based and a sentence embedding based. Ngram orders and 
thresholds can be manually specified.

    usage: align.py [-h] [--scoring {ngram,sentence embedding}] [--ngram-order NGRAM_ORDER] [--model MODEL] [--threshold THRESHOLD] [--lowercase]
                [--stopwords] [--mode {evaluate,align}]
                infile outfile

    positional arguments:
      infile                path to the sentence segmented file
      outfile               path to the file with the similarity matrices

    optional arguments:
      -h, --help            show this help message and exit
      --scoring {ngram,sentence embedding}
      --ngram-order NGRAM_ORDER
      --model MODEL         a string specifying a SentenceTransformers model
      --threshold THRESHOLD
      --lowercase           sentences are lowercased before similarity score is computed
      --stopwords           remove stopwords before similarity score is calculated
      --mode {evaluate,align}


### Evaluation
To replicate the evaluation I performed, the shell scripts in scripts/evaluate can be used.

To produce the aligned test files for the ngram based approach, use:

    ./scripts/evaluate/align_ng4-6_th002-016.sh
    
For the semantic similarity based approach, use:

    ./scripts/evaluate/align_st_th01-06.sh
    
To compute Precision, Recall and F1 score for all the produced test files:

    ./scripts/evaluate/evaluate.sh