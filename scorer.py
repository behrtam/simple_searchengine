import string

from math import log10, sqrt
from collections import defaultdict

#TODO: refactor to utils class
def normalized_word_frequency(text, stopwords):
    table = str.maketrans("", "", string.punctuation)
    hist = defaultdict(int)
    for term in [word.lower() for word in text.translate(table).split() if word.lower() not in stopwords]:
        hist[term] += 1
    return hist


class Scorer:
    def __init__(self, index):
        self.index = index

    def calculate_scores(self, query):
        scores = defaultdict(int)
        query_terms = normalized_word_frequency(query, self.index.stopwords)
        query_length = 0

        for term in query_terms:
            postings = self.index.term_weight[term]

            # we assume that every term in a query only occures once
            # so the tf part would look like this: (1 + log10(1)) => 1
            tf_idf_tq = log10(len(self.index.documents_length) / self.index.document_frequency[term]);

            query_length += (tf_idf_tq ** 2)

            for document, tf_idf_td in postings:
                scores[document] += (tf_idf_tq * tf_idf_td)

        # length normalization
        for doc in scores:
            scores[doc] = scores[doc] / (self.index.documents_length[doc] * sqrt(query_length))

        return scores
