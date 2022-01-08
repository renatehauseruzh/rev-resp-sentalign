import csv
import json
import argparse
import spacy
import similarity_v3
import convert_format_v2


class Aligner():
    # only one instance of this should be created at the beginning of the process

    def __init__(self, threshold):
        self.threshold = threshold

    def extract_alignments(self, sim_matrix):
        """
        for a given similarity matrix of a document, extract the alignments
        :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, revsent_id2: {...} }
        :return: dicts with sentence IDs as keys and alignment IDs as values?
        """

        candidates = self._get_candidates(sim_matrix=sim_matrix)

        # format of alignments: [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        buckets = []
        while candidates:
            # get first element in the list
            el = candidates.pop(0)

            # if only one element was left, this forms a bucket by itself
            if len(candidates) == 0:
                bucket = [el]
                buckets.append(bucket)
            # put all alignments that have either same resp_id or rev_id than first element into a bucket
            #bucket = [(rev, resp) for (rev, resp) in candidates if rev == el[0] or resp == el[1]]
            else:
                bucket = [el]
                leftover = []
                for rev, resp in candidates:
                    if rev == el[0] or resp == el[1]:
                        bucket.append((rev, resp))
                    else:
                        leftover.append((rev, resp))

                # save bucket to a list
                buckets.append(bucket)
                # only keep on searching in candidates that don't belong to any bucket yet
                candidates = leftover

        alignments = {}
        i = 1
        for bucket in buckets:
            # each bucket gets a unique alignment ID
            aid = str(i)
            alignments[aid] = {'review': [], 'response': []}
            for rev, resp in bucket:
                if rev not in alignments[aid]['review']:
                    alignments[aid]['review'].append(rev)
                if resp not in alignments[aid]['response']:
                    alignments[aid]['response'].append(resp)
            i += 1
        return alignments

    def _get_candidates(self, sim_matrix):
        """
        Get all rev-resp pairs that have a similarity above the specified threshold
        :param sim_matrix: dict of format {revsent_id1: {resp_id1: sim1, resp_id2: sim2}, rev_sent_id2: {...}}
        :return alignments: list of format [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        """
        alignments = []
        for rev_sent_id, responses in sim_matrix.items():

            for resp_sent_id, sim in responses.items():
                if sim >= self.threshold:
                    alignments.append((rev_sent_id, resp_sent_id))
        return alignments


###########################################################################################
# UTILITY FUNCTIONS FOR READING AND WRITING FILES
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
            rev_sents, resp_sents = list(rev_doc.sents), list(resp_doc.sents)

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
    #parser.add_argument('--out-format', choices=['tsv', 'json'], default='json')
    parser.add_argument('--ngram-order', type=int, default=6)  # default=6 in Popovic, 2015
    parser.add_argument('--threshold', type=float, default=0.5) # TODO: has to be investigated
    parser.add_argument('--mode', choices=['evaluate', 'align'], default='evaluate') # TODO: change default to align later

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    aligner = Aligner(args.threshold)
    simc = similarity_v3.Similarity(args.ngram_order)

    if args.mode == 'evaluate':
        converter = convert_format_v2.FormatConverter(infile=args.infile, outfile=args.outfile, delimiter='\t')
        data = converter.convert_data()
    else:
        # generator
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

        json.dump(aligned, outf, indent=4) # format could also be changed to jsonl if data is too big to hold in memory


if __name__ == '__main__':
    main()










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