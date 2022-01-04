import argparse
import json
import csv


# TODO: CLI that takes:
#   - filenames
#       - infile similarities (json)
#       - infile split sentences (json)
#       - outfile (tsv)
#   - threshold (?)



# TODO: extract alignments
#   - find all above threshold
#   - assign alignment IDs
#   - save in suitable data structure


class Aligner():

    def __init__(self, threshold, corpus_filename):
        self.threshold = threshold
        self.alignment_id = 0
        with open(corpus_filename, 'r', encoding='utf-8') as infile:
            self.sent_split_corpus = json.load(infile)

    # TODO: receive similarities in json format with IDs only

    # TODO: for each doc, extract all pairs that have similarity above threshold


    # TODO: assign unique alignment ID:
    #   - 1-to-1: assign ID if one rev sent has exactly one resp sent above threshold
    #   - 1-to-many: if one rev sent has several resp sents above threshold: same ID
    #   - many-to-1: if several rev sents have the same resp sent above threshold: same ID
    #   - many-to-many:
    #   -
    #   -

    def get_alignments(self, doc):
        # format of doc: {rev_sent_id1: {resp_id1: sim1, resp_id2: sim2}, rev_sent_id2: {resp_id1: sim3, resp_id2: sim4}}
        alignments = []
        for rev_sent_id, responses in doc.items():

            for resp_sent_id, sim in responses.items():
                if sim >= self.threshold:
                    alignments.append((rev_sent_id, resp_sent_id))

        return alignments

    def assign_alignment_ids(self, alignments, doc_id):
        # format of alignments: [(rev_id1, resp_id2), (rev_id1, resp_id3), (rev_id2, resp_id4)]
        buckets = []
        while alignments:
            # get first element in the list
            el = alignments.pop(0)
            # put all alignments that have either same resp_id or rev_id than first element into a bucket
            bucket = [(rev, resp) for (rev, resp) in alignments if rev==el[0] or resp==el[1]]
            bucket.append(el)
            # save bucket to a list
            buckets.append(bucket)

        for bucket in buckets:
            # each bucket gets an alignment ID
            self.alignment_id += 1
            for alignment in bucket:
                # find the review and response sentence in the corpus and save alignment ID along with them
                self.sent_split_corpus[doc_id][alignment[0]]['UAID'] = self.alignment_id
                self.sent_split_corpus[doc_id][alignment[1]]['UAID'] = self.alignment_id

    def write_tsv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as outf:
            # headers
            tsv_writer = csv.writer(outf, delimiter='\t')
            tsv_writer.writerow(['DOCID', 'REVIEW SENTID', 'REVIEW SENT', 'REVIEW AUID', 'RESPONSE SENTID', 'RESPONSE SENT', 'RESPONSE AUID'])

            for doc_id in self.sent_split_corpus.keys():
                # as many lines as the longer list (rev or resp) is long
                length_rev = len(self.sent_split_corpus[doc_id]['rev'].keys())
                length_resp = len(self.sent_split_corpus[doc_id]['resp'].keys())
                longer = length_rev if length_rev >= length_resp else length_resp
                i = 0
                # write a row for each sentence in rev and resp
                while i < longer:
                    rev_id = self.sent_split_corpus[doc_id]['rev'].keys()[i]
                    resp_id = self.sent_split_corpus[doc_id]['resp'].keys()[i]

                    rev_sent = self.sent_split_corpus[doc_id]['rev'][rev_id]['sent']
                    resp_sent = self.sent_split_corpus[doc_id]['resp'][resp_id]['sent']

                    rev_uaid = self.sent_split_corpus[doc_id]['rev'][rev_id]['UAID']
                    resp_uaid = self.sent_split_corpus[doc_id]['resp'][resp_id]['UAID']

                    row = (doc_id, rev_id, rev_sent, rev_uaid, resp_id, resp_sent, resp_uaid)
                    tsv_writer.writerow(row)
