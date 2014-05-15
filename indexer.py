import string

from collections import defaultdict
from math import log10, sqrt

class Indexer:
    def __init__(self, contents, stopwords):
        self.contents = contents
        self.stopwords = stopwords

        self.normalized_contents = []

        self.term_frequency = defaultdict(list)
        self.document_frequency = defaultdict(int)
        self.term_weight = defaultdict(list)
        self.documents_length = defaultdict(int)

    def normalize(self):
        table = str.maketrans("", "", string.punctuation)
        for url, content in self.contents:
            terms = [term.lower() for term in content.translate(table).split() if term.lower() not in self.stopwords]
            self.normalized_contents.append((url, terms))

    def calculate_frequency_distribution(self, normalized_content):
        hist = defaultdict(int)

        for term in normalized_content:
            hist[term] += 1

        return hist

    def build_index(self):
        self.normalize()
        
        for url, content in self.normalized_contents:
            term_freq = self.calculate_frequency_distribution(content)

            for term, freq in term_freq.items():
                self.document_frequency[term] += 1
                self.term_frequency[term].append((url, freq))

        self.calculate_weight()
        self.calculate_document_length()

    # cacluates dampend tf-idf weight for each term
    def calculate_weight(self):
        N = len(self.normalized_contents)
        for term, value in self.term_frequency.items():
            idf = log10(N / self.document_frequency[term])
            for doc, tf in value:
                tfidf = (1 + log10(tf)) * idf
                self.term_weight[term].append((doc, tfidf))


    def calculate_document_length(self):
        for term, value in self.term_weight.items():
            for doc, weight in value:
                self.documents_length[doc] += weight ** 2

        for doc in self.documents_length:
            self.documents_length[doc] = sqrt(self.documents_length[doc])








