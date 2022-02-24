# rev-resp-sentalign

## Requirements

- The following commands work in a unix-like system with bash
- Python 3 must be installed on your system
- Install the requirements specified in requirements.txt


The following commands are executed from rev-resp-alignment as working directory

## Alignment
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


## Data
### Input format
The input data for the alignment is a dataset compiled from review-response pairs for hotels published on TripAdvisor.
It is in csv format and contains the following fields:

    doc_id,domain,rating,review_author,response_author,review_clean,response_clean,sentiment,db_internal_id,establishment,trip_id,trip_url,country,split,score:review_response_length_ratio,score:response_sentence_length,score:genericness_semantic_avg,score:genericness_length_ratio,score:review_response_wmd,rrgen_id	

However, for our purposes, only the fields "doc_id", "review_cleaned", and "response_cleaned"
are relevant.

### Output format
The output is formatted in json and contains the sentence splitted review and response
and the alignments. Each alignment consists of a tuple of review sentence indices and corresponding
response sentence indices.

    {
            "doc_id": "3173251",
            "review": [
                "Very good hotel ---SEP--- Stayed here for work for one night.",
                "Staff were extremely friendly, greeting me as I got out of the lift (reception is on 1st floor) and asking lots of genuine questions about why I was there and how they could help.",
                "Room was possibly the cleanest I have ever stayed in, but didn't' appear to have a window until I found it hidden behind a wardrobe in the small alcove at the back right of the room.",
                "Even then it only overlooked a small light well about 12 foot wide but which was so tall I couldn't actually see sky/the weather at the top!",
                "Weirder still you look straight into other rooms which made me close the curtains to my room despite it only being mid afternoon, so there was essentially no window in the room.",
                "This is my only criticism, and a fairly minor one at that.",
                "Decor is quirky but functional and the free breakfast is plentiful and tasty.",
                "Location is excellent, just a few minutes from both main train stations and a few steps from the shopping and most main areas.",
                "I had a good nights sleep and really appreciated the USB socket next to the.bed for phone chargers!"
            ],
            "response": [
                "Hello KatMcP",
                "Firstly, great to hear your room was super clean, ill let the housekeeping team and Klaudia know( they probably read this as they all do) Some of our rooms are a bit of a weird shape its true, this is due to the nature of the building and as such we have tried to make the most of natural light and the space itself.",
                "We are a square building",
                "so yes, some rooms look onto others, these internal rooms are the favourites of the \"in the know\" guests who like a deep sleep as they are silent.",
                "You can always draw the net curtain for privacy while still allowing for natural light.",
                "Sounds like everything else was peachy though.",
                "God times.",
                "My best Rory"
            ],
            "alignment": [
                [
                    [
                        "4"
                    ],
                    [
                        "3"
                    ]
                ],
                [
                    [
                        "2"
                    ],
                    [
                        "1"
                    ]
                ]
            ]
        },


## Evaluation
To replicate the evaluation I performed, the shell scripts in scripts/evaluate can be used.

To produce the aligned test files for the ngram based approach, use:

    ./scripts/evaluate/align_ng4-6_th002-016.sh
    
For the semantic similarity based approach, use:

    ./scripts/evaluate/align_st_th01-06.sh
    
To compute Precision, Recall and F1 score for all the produced test files:

    ./scripts/evaluate/evaluate.sh
    
    
### Goldstandard
To measure the performance of the candidate Aligners, we evaluate them against a manually annotated goldstandard
that contains 115 review-response pair documents.
The annotated goldstandard can be found in:

    data/goldstandard/rev-resp-goldstandard_annotated_115.csv
    data/goldstandard/rev-resp-goldstandard_annotated_115.json

#### Inter-Annotator Agreement
To measure the reliability of the annotations in the goldstandard, both annotators annotated the complete goldstandard.
The double annotated goldstandard can be found in:
    
    data/goldstandard/rev-resp-goldstandard_double_annotated_115.csv

The inter-annotator agreement can be computed using the script iaa.py. You can either compute
Cohen's Kappa:
    
    K = (Po - Pe) / (1 - Pe)
    
Or with:

    Agreement = (2 * I) / (A1 + A2)
    Where A1 and A2 are the number of True instances for the annotation 1 and annotation 2, respectively
    and I is the intersection of the two annotations
    
Use the script as follows:

    usage: iaa.py [-h] --gs_file GS_FILE --metric {cohens-k,agr}

    optional arguments:
      -h, --help                show this help message and exit
      --gs_file GS_FILE         path to the double annotated gold standard
      --metric {cohens-k,agr}   the metric to compute the IAA
