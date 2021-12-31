import argparse
from collections import Counter
from nltk.util import ngrams


class Similarity():

    def read_data(self, filename):
        # TODO: read in doc
        # read into which format?
        # {rev: [sent1, sent2, sent3], resp: [sent1, sent2]}
        ...

    def calculate_similarities(self, doc):
        # TODO: per document, produce matrix
        # get doc {rev: [sent1, sent2, sent3], resp: [sent1, sent2]}
        longer = doc['rev'] if len(doc['rev']) >= len(doc['resp']) else doc['resp']
        shorter = doc['rev'] if len(doc['rev']) < len(doc['resp']) else doc['resp']

        for seg_l in longer:
            for seg_s in shorter:
                similarity = self.chrF(seg_l, seg_s)

        # TODO: format?
        return similarity_matrix

    def create_ngrams(self, sent, n):
        ngram_tups = ngrams(sent, n)
        grams = ["".join(tup) for tup in ngram_tups]
        return grams

    def chrF(self, ref_sent, hyp_sent, order):

        ref_ngrams = self.create_ngrams(ref_sent, order)
        hyp_ngrams = self.create_ngrams(hyp_sent, order)

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

        chrP = overlap_count / len(hyp_ngrams)
        chrR = overlap_count / len(ref_ngrams)

        chrF = 2 * ((chrP * chrR) / (chrP + chrR))
        return chrF


    def write_data(self, filename):
        # TODO: save in tsv format
        ...


# command line interface
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('infile', help="path to the raw goldstandard file")
    parser.add_argument('outfile', help="path to the new goldstandard tsv file")

    args = parser.parse_args()
    return args


def main():
    ...


if __name__ == '__main__':
    main()