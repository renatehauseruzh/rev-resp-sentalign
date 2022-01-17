import argparse
import json
import csv
from collections import Counter
from nltk.util import ngrams


class Similarity():

    def __init__(self, order):
        self.order = order

    def calculate_similarities(self, doc):
        # get doc in following format: {rev: {sent_id1: sent1, sent_id2: sent2}, resp: {resp_sentid1: resp_sent1, resp_sentid2: resp_sent2}}
        # get doc as Document object
        similarity_matrix = {}  # {rev_id1: {resp_id1: 0.0, resp_id2: 0.1}, rev_id2: {resp_id1: 0.2, resp_id2: 0.3}}
        for rev_id, rev_sent in doc.rev_sents.items():
            similarities = {}
            for resp_id, resp_sent in doc.resp_sents.items():
                similarity = self._chrF(rev_sent, resp_sent)
                similarities[resp_id] = similarity
            similarity_matrix[rev_id] = similarities
        return similarity_matrix  # {rev_id1: {resp_id1: 0.0, resp_id2: 0.1}, rev_id2: {resp_id1: 0.2, resp_id2: 0.3}}

    def _create_ngrams(self, sent):
        ngram_tups = ngrams(sent, self.order)
        grams = ["".join(tup) for tup in ngram_tups]
        return grams

    def _chrF(self, ref_sent, hyp_sent):

        ref_ngrams = self._create_ngrams(ref_sent)
        hyp_ngrams = self._create_ngrams(hyp_sent)

        ref_ngram_counts = Counter(ref_ngrams)
        hyp_ngram_counts = Counter(hyp_ngrams)

        overlap_count = 0
        for ngram in hyp_ngram_counts.keys():
            # wenn es nicht existiert, nicht zählen
            if ngram not in ref_ngram_counts.keys():
                continue
            # wenn es existiert, und weniger oder gleich oft vorkommt wie in ref += dieser value
            if hyp_ngram_counts[ngram] <= ref_ngram_counts[ngram]:
                overlap_count += hyp_ngram_counts[ngram]
            # wenn es öfter vorkommt als in ref += value von ref
            elif hyp_ngram_counts[ngram] > ref_ngram_counts[ngram]:
                overlap_count += ref_ngram_counts[ngram]

        chrP = overlap_count / len(hyp_ngrams) if len(hyp_ngrams) > 0 else 0
        chrR = overlap_count / len(ref_ngrams) if len(ref_ngrams) > 0 else 0

        if chrP == 0 and chrR == 0:
            return 0
        else:
            chrF = 2 * ((chrP * chrR) / (chrP + chrR))
            return chrF


def read_data(filename):
    # {doc1: {rev: {sent_id1: sent1, sent_id2: sent2}, resp: {resp_sentid1: resp_sent1, resp_sentid2: resp_sent2}}}
    data = {}
    with open(filename, 'r', encoding='utf-8') as inf:
        reader = csv.reader(inf, delimiter='\t')
        for line in reader:
            # skip empty dividing lines
            if not line:
                continue
            # get relevant data from line
            document_id = str(line[0])
            rev_sent_id = str(line[1]) if line[1] else None
            rev_sent = line[2]
            resp_sent_id = str(line[4]) if line[4] else None
            resp_sent = line[5]
            # add all sentences of one document to the dictionary entry of the document ID
            if document_id in data.keys():
                if rev_sent_id is not None:
                    data[document_id]['rev'][rev_sent_id] = rev_sent
                if resp_sent_id is not None:
                    data[document_id]['resp'][resp_sent_id] = resp_sent
            # if a new document starts, initialize new dict for document ID
            else:
                data[document_id] = {'rev': {rev_sent_id: rev_sent}, 'resp': {resp_sent_id: resp_sent}}
    return data


def write_data(filename, data):
    # TODO: write in tsv format
    # write in json format
    with open(filename, 'w', encoding='utf-8') as outf:
        json.dump(data, outf, indent=4)


# command line interface
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the sentence segmented file")
    parser.add_argument('outfile', help="path to the file with the similarity matrices")
    parser.add_argument('--out-format', choices=['tsv', 'json'], default='json')
    parser.add_argument('--ngram-order', default=6)  # default as in Popovic, 2015

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    sim = Similarity(order=args.ngram_order)
    data = read_data(
        args.infile)  # {doc1: {rev: {sent_id1: sent1, sent_id2: sent2}, resp: {resp_sentid1: resp_sent1, resp_sentid2: resp_sent2}}}

    corpus_with_sim = {}
    for doc_id, doc in data.items():
        similarity_matrix = sim.calculate_similarities(doc)
        corpus_with_sim[doc_id] = similarity_matrix

    write_data(args.outfile, corpus_with_sim)


if __name__ == '__main__':
    main()
