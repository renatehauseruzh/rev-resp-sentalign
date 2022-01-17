from collections import Counter
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from gensim.parsing.preprocessing import remove_stopwords
from sentence_transformers import SentenceTransformer, util



class Similarity():

    def __init__(self, order, lowercase=False, stopwords=False):
        self.order = order
        self.lowercase = lowercase
        self.remove_stopwords = stopwords

    def calculate_similarities(self, doc):
        # get doc in following format: {'doc_id': id, 'review': ['asdfa', 'asdfa'], 'response': ['fasdf', 'fds'¨]
        similarity_matrix = {}  # {rev_id1: {resp_id1: 0.0, resp_id2: 0.1}, rev_id2: {resp_id1: 0.2, resp_id2: 0.3}}
        for rev_id, rev_sent in enumerate(doc['review']):
            similarities = {}
            for resp_id, resp_sent in enumerate(doc['response']):
                similarity = self._chrF(rev_sent, resp_sent)
                similarities[resp_id] = similarity
            similarity_matrix[rev_id] = similarities
        return similarity_matrix  # {rev_id1: {resp_id1: 0.0, resp_id2: 0.1}, rev_id2: {resp_id1: 0.2, resp_id2: 0.3}}

    def _create_ngrams(self, sent):
        if self.lowercase:
            sent = sent.lower()
        if self.remove_stopwords:
            #sent = " ".join([w for w in word_tokenize(sent) if w not in stopwords.words('english')])
            sent = remove_stopwords(sent)
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


class SentTransformerSimilarity():

    def __init__(self, model):
        # ev. model?
        self.model = SentenceTransformer(model) # sentence-transformers/nli-mpnet-base-v2  'sentence-transformers/paraphrase-MiniLM-L3-v2'

    def calculate_similarities(self, doc):
        # get doc in following format: {'doc_id': id, 'review': ['asdfa', 'asdfa'], 'response': ['fasdf', 'fds'¨]

        review = doc['review']
        response = doc['response']

        #print(len(review))
        if not review:
            return {}

        rev_embeddings = self.model.encode(review, convert_to_tensor=True)
        resp_embeddings = self.model.encode(response, convert_to_tensor=True)

        cosine_scores = util.cos_sim(rev_embeddings, resp_embeddings)
        similarity_matrix = {}
        for rev_id, resps in enumerate(cosine_scores):

            similarities = {}
            for resp_id, score in enumerate(resps):
                similarities[str(resp_id)] = score
            similarity_matrix[str(rev_id)] = similarities

        return similarity_matrix

def main():
    doc = {
        "doc_id": "3287424",
        "review": [
            "Beautiful views and convenient location ---SEP--- Our family of 4 had a lovely one-night stay.",
            "We stayed in a 2BR unit which had stunning views of the valley.",
            "It was quite spacious and comfortable.",
            "I will add that the d\u00e9cor seemed a bit worn.",
            "We had a very pleasant check-in and were impressed by the woman at reception who was managing two surly guests with grace while we waited.",
            "The complaints we heard were ridiculous and she was so composed.",
            "She checked us in quickly and in a friendly manner.",
            "We enjoyed a the walking trail around the property and our teen girls liked the giant chess game on the lawn.",
            "We had dinner at Rae's, which was delicious and allowed for an incredible view as well.",
            "The estate is well located near wineries and the chocolatier and was a easy drive to our early balloon flight."
        ],
        "response": [
            "Dear ClaireJourneys, Thank you for taking the time to review your stay at Balgownie Estate.",
            "It is great to see that you were able to enjoy a family getaway with us at the Estate.",
            "We are working towards renovating all our rooms at the Estate to keep them fresh and appealing for all guests during their stay.",
            "I have also passed your kind words on to our Rae's Restaurant after you enjoyed your meal with us.",
            "We hope to welcome you and your family back for another visit soon.",
            "Kind Regards Charlotte"
        ],
        "alignment": []
    }

    doc2 = {
            "doc_id": "3271710",
            "review": [
                "Fabulous location ---SEP---",
                "I really enjoyed this hotel.",
                "It was a surprising find at the end of a very busy and long day.",
                "Great surrounds - lake on one side, a beach on the other, with friendly and helpful staff.",
                "The bed was so comfortable too!"
            ],
            "response": [
                "Thank you for taking time to provide feedback on your recent stay.",
                "It is pleasing to hear that you really enjoyed your stay with us, along with our unbeatable location with Narrabeen Beach on one side and Narrabeen Lake on the other.",
                "Furthermore, it is great to hear you had a great nights sleep in our comfortable beds, and found our team to be friendly and helpful.",
                "We look forward to the opportunity of welcoming you back again in the future.",
                "Kind regards, Anita Reskov Front Office & Reservations Manager Quality Hotel Sands"
            ],
            "alignment": []
        }

    sim = SentTransformerSimilarity()

    cosine_scores = sim.calculate_similarities(doc2)

    print(cosine_scores)


if __name__ == '__main__':
    main()
