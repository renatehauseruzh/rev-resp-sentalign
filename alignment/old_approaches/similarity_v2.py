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