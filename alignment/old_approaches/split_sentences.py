import csv
import json
import spacy
import argparse


class SentenceSplitter():

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.nlp = spacy.load('en_core_web_md')
        self.rev_sent_id = 50000000
        self.resp_sent_id = 80000000

    # get structure: {doc_id: [[(rev_sentID, rev_sent, None/''), (resp_sentID, resp_sent, None/'')][(rev_sentID, rev_sent, None/''), ('', '', '')
    def split_sentences(self):
        segmented = {}
        with open(self.infile, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter=',')
            for line in reader:
                # get relevant data from the line
                document_id = line[0]
                review = line[5]
                response = line[6]

                # for each doc start sentence ids with the next number divisible by 10
                if (self.rev_sent_id % 10) != 0:
                    rest = 10 - (self.rev_sent_id % 10)
                    self.rev_sent_id += rest
                if (self.resp_sent_id % 10) != 0:
                    rest = 10 - (self.resp_sent_id % 10)
                    self.resp_sent_id += rest


                rev_doc = self.nlp(review)
                resp_doc = self.nlp(response)
                rev_sents, resp_sents = [], []

                # do the sentence segmentation of the review doc
                for sent in rev_doc.sents:
                    sent_tup = (self.rev_sent_id, sent.text, '')
                    rev_sents.append(sent_tup)
                    # increment sentence ID
                    self.rev_sent_id += 1
                # do the sentence segmentation of the response doc
                for sent in resp_doc.sents:
                    sent_tup = (self.resp_sent_id, sent.text, '')
                    resp_sents.append(sent_tup)
                    # increment sentence ID
                    self.resp_sent_id += 1

                # pad with empty tuples so that documents can be aligned nicely in the tsv
                if len(rev_sents) != len(resp_sents):
                    # pad review document
                    if len(rev_sents) < len(resp_sents):
                        i = len(rev_sents)
                        while i < len(resp_sents):
                            rev_sents.append(('', '', ''))
                            i += 1
                    # pad response document
                    elif len(rev_sents) > len(resp_sents):
                        i = len(resp_sents)
                        while i < len(rev_sents):
                            resp_sents.append(('', '', ''))
                            i += 1

                segmented[document_id] = zip(rev_sents, resp_sents)
        return segmented

    def write_tsv(self):
        with open(self.outfile, 'w', newline='', encoding='utf-8') as outf:
            # headers
            tsv_writer = csv.writer(outf, delimiter='\t')
            tsv_writer.writerow(['DOCID', 'REVIEW SENTID', 'REVIEW SENT', 'REVIEW AUID', 'RESPONSE SENTID', 'RESPONSE SENT', 'RESPONSE AUID'])

            # get dictionary with doc ids and segmented sentences
            segmented = self.split_sentences()

            # concatenate doc id, review sentence and response sentence to form a new row
            for doc_id, sents in segmented.items():
                for sent in sents:
                    row = (doc_id,) + sent[0] + sent[1]
                    tsv_writer.writerow(row)
                tsv_writer.writerow('')


# TODO: ev. find common functionality
# TODO: class to split and write json(l)
class SentenceSplitterJson():

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.nlp = spacy.load('en_core_web_md')

    def split_sentences(self):
        segmented = []
        with open(self.infile, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter=',')
            for line in reader:
                # get relevant data from the line
                document_id = line[0]
                review = line[5]
                response = line[6]
            # do sentence segmentation
            rev_doc = self.nlp(review)
            resp_doc = self.nlp(response)
            rev_sents, resp_sents = list(rev_doc.sents), list(resp_doc.sents)
            # save segmented document in json datastructure (dict)
            seg_doc = {'doc_id': document_id, 'review': rev_sents, 'response': resp_sents}
            segmented.append(seg_doc)
        return segmented

    def write_json(self, segmented):
        with open(self.outfile, 'w', encoding='utf-8') as outf:
            json.dump(segmented, outf, indent=4)






# command line interface
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the raw goldstandard file")
    parser.add_argument('outfile', help="path to the new goldstandard tsv file")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    splitter = SentenceSplitter(infile=args.infile, outfile=args.outfile)
    splitter.write_tsv()


if __name__ == '__main__':
    main()