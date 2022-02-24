import csv
import json
import argparse
import spacy
import time
import nltk
import similarity
import convert_format
from itertools import groupby


class Aligner():
    # only one instance of this should be created at the beginning of the process

    def __init__(self, threshold):
        self.threshold = threshold

    def extract_alignments(self, sim_matrix): #sim_matrix
        candidates = self._get_candidates(sim_matrix=sim_matrix)
        # sort by review ids
        key_func = lambda x: x[0]
        rev_resp_pairs = []
        # key is the review id, group contains all rev-resp sentence pairs that contain the key review ID
        for key, group in groupby(candidates, key_func):
            # append a tuple to rev_resp_pairs: (["revid1"], ["respid1", "respid2", "respid3"])
            rev_resp_pairs.append(([key], [i[1] for i in group]))

        # create n:m-alignments
        buckets = []
        while rev_resp_pairs:
            # create a new n:m-alignment (bucket)
            el = rev_resp_pairs.pop()
            bucket = [set(el[0]), set(el[1])]
            leftover = []
            for rev, resp in rev_resp_pairs:
                # if there is an overlap of resp sents in the bucket and in the candidate, add review id and response ids to this bucket
                if bool(bucket[1] & set(resp)):
                    # add review and response sentences to the n:m-alignment
                    bucket[0].update(rev)
                    bucket[1].update(resp)
                else:
                    leftover.append((rev, resp))
            bucket = [list(bucket[0]), list(bucket[1])]
            buckets.append(bucket)
            # keep on producing alignments with the remaining pairs
            rev_resp_pairs = leftover
        return buckets

    def _get_candidates(self, sim_matrix):
        """
        Get all rev-resp pairs that have a similarity above the specified threshold
        :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, rev_sent_id2: {...}}
        :return alignments: list of format [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        """
        alignments = []
        for rev_sent_id, responses in sim_matrix.items():
            # if similarity score is above threshold, this is a candidate
            for resp_sent_id, sim in responses.items():
                if sim >= self.threshold:
                    alignments.append((str(rev_sent_id), str(resp_sent_id)))
        return alignments


###########################################################################################
# UTILITY FUNCTION FOR READING FILES
###########################################################################################
def read_and_split_data(filename):
    """
    Read in data from csv corpus file and split sentences
    :param filename:
    :return:
    """
    nlp = spacy.load('en_core_web_md')
    with open(filename, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=',')
        for line in reader:
            doc_data = {}
            # get relevant data from the line
            document_id = str(line[0])
            review = line[5]
            response = line[6]
            # do sentence segmentation
            rev_doc = nlp(review)
            resp_doc = nlp(response)
            #rev_sents, resp_sents = list(rev_doc.sents), list(resp_doc.sents)
            rev_sents = [str(sent) for sent in rev_doc.sents]
            resp_sents = [str(sent) for sent in resp_doc.sents]

            doc_data['doc_id'] = document_id
            doc_data['review'] = rev_sents
            doc_data['response'] = resp_sents

            yield doc_data



###########################################################################################
# COMMAND LINE INTERFACE
###########################################################################################


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the sentence segmented file")
    parser.add_argument('outfile', help="path to the file with the similarity matrices")
    parser.add_argument('--scoring', choices=['ngram', 'sentence embedding'], default='ngram')
    parser.add_argument('--ngram-order', type=int, default=6)  # default=6 in Popovic, 2015
    parser.add_argument('--model', type=str, default='sentence-transformers/nli-mpnet-base-v2', help="a string specifying a SentenceTransformers model")
    parser.add_argument('--threshold', type=float, default=0.4)
    parser.add_argument('--lowercase', action='store_true', help="sentences are lowercased before similarity score is computed")
    parser.add_argument('--stopwords', action='store_true', help='remove stopwords before similarity score is calculated')
    parser.add_argument('--mode', choices=['evaluate', 'align'], default='evaluate') # TODO: change default to align later

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    #nltk.download('punkt')
    #nltk.download('stopwords')

    aligner = Aligner(args.threshold)

    # similarity scoring strategy
    if args.scoring == 'ngram':
        simc = similarity.Similarity(args.ngram_order, args.lowercase, args.stopwords)
    else:
        simc = similarity.SentTransformerSimilarity(args.model)

    # if it is in evaluate mode, the goldstandard files need to be converted, data is loaded into memory
    if args.mode == 'evaluate':
        converter = convert_format.FormatConverter(infile=args.infile, outfile=args.outfile, delimiter=',')
        data = converter.convert_data()
    else:
        # if large file should be aligned, generator so that not all data is loaded into memory
        data = read_and_split_data(args.infile)

    with open(args.outfile, 'w', encoding='utf-8') as outf:
        aligned = []
        for doc in data:
            # doc is a dict: {'doc_id': id, 'review': ['asdkjf', 'sadfas', 'asdfasd'], 'response': ['resrs', 'resrs']}

            similarities = simc.calculate_similarities(doc=doc)

            # extract alignments
            alignments = aligner.extract_alignments(sim_matrix=similarities)

            doc['alignment'] = alignments

            aligned.append(doc)
        # TODO: make other metadata for senttransformer
        aligned_file = {'meta': {'n-gram order': args.ngram_order, 'threshold': args.threshold}, 'alignment': aligned}
        json.dump(aligned_file, outf, indent=4) # format could also be changed to jsonl if data is too big to hold in memory


if __name__ == '__main__':
    main()
    #aligner = Aligner(threshold=0.5)
    #candidates = [(0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 4), (3, 5)]
    #alignments = aligner.extract_alignments_v2(candidates)
    #print(alignments)











##########################################################
# id_bucket = []
#             for i in range(0, len(candidates)):
#                 rev = candidates[i][0]
#                 resp = candidates[i][1]
#                 if rev == el[0] or resp == el[1]:
#                     id_bucket.append(i)
#
#             for id in id_bucket:
#                 pair = candidates[id]
#                 bucket.append(pair)
#
#             for id in id_bucket:
#                 candidates.remove(id)
#             bucket.append(el)




#         for bucket in buckets:
#             # each bucket gets a unique alignment ID
#             aid = str(i)
#             alignments[aid] = {'review': [], 'response': []}
#             for rev, resp in bucket:
#                 if rev not in alignments[aid]['review']:
#                     alignments[aid]['review'].append(rev)
#                 if resp not in alignments[aid]['response']:
#                     alignments[aid]['response'].append(resp)
#             i += 1
#         return alignments





#     def extract_alignments_v2(self, sim_matrix):
#         """
#         for a given similarity matrix of a document, extract the alignments
#         :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, revsent_id2: {...} }
#         :return: buckets: list of the format [ [[revid1, revid2], [respid1]], [[revid3], [respid2, respid3]], ...]
#         """
#
#         # extract all candidate pairs where similarity score is above threshold
#         candidates = self._get_candidates(sim_matrix=sim_matrix)
#
#         # format of alignments: [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
#         buckets = []
#         while candidates:
#             # get first element in the list to compare rest of the list to it
#             el = candidates.pop(0)
#
#             # if only one element was left, this forms a bucket by itself
#             if len(candidates) == 0:
#                 bucket = [el]
#                 buckets.append(bucket)
#             # put all alignments that have either same resp_id or rev_id as first element into a bucket
#             else:
#                 bucket = [[el[0]], [el[1]]]
#                 leftover = []
#                 while candidates != leftover:
#                     candidates = leftover
#                     leftover = []
#                     for rev, resp in candidates:
#                         if rev in bucket[0] or resp in bucket[1]:
#                             bucket[0].append(rev)
#                             bucket[1].append(resp)
#                         #if rev == el[0] or resp == el[1]:
#                         #    bucket.append((rev, resp))
#                         else:
#                             leftover.append((rev, resp))
#
#                 # save bucket to a list
#                 buckets.append(bucket)
#                 # only keep on searching in candidates that don't belong to any bucket yet
#                 candidates = leftover
#
#         return buckets