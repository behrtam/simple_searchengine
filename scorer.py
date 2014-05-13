import string

from math import log10, sqrt
from collections import defaultdict

#TODO: refactor to utils class
def normalize(text, stopwords):
    table = str.maketrans("", "", string.punctuation)
    return [word.lower() for word in text.translate(table).split() if word.lower() not in stopwords]


class Scorer:
	def __init__(self, term_frequency, documents_length, document_count, stopwords):
		self.term_frequency = term_frequency
		self.documents_length = documents_length
		self.document_count = document_count
		self.stopwords = stopwords

	def calculate_scores(self, query):
		scores = defaultdict(int)

		query_terms = normalize(query, self.stopwords)

		for term in query_terms:
			postings = self.term_frequency[term]

			for document, term_frequency in postings:

				# Term Frequency and Inverse Document Frequency of Term in Document
				tf_idf_td = (1 + log10(term_frequency)) * log10(self.document_count / len(postings))

				# Term Frequency and Inverse Document Frequency of Term in Query
				tf_idf_tq = log10(self.document_count / len(postings))

				scores[document] += tf_idf_td * tf_idf_tq

		norm_q = len(query_terms)

		cos_score = {}

		for doc, score in scores.items():
			norm_d = self.documents_length[doc]

			cos_score[doc] = (score / (norm_q * norm_d))


		return cos_score 

