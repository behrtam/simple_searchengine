import string

from collections import defaultdict

class Indexer:
    def __init__(self, contents, stopwords):
        self.contents = contents
        self.stopwords = stopwords

        self.normalized_contents = []

        self.term_frequency = defaultdict(list)
        self.document_frequency = defaultdict(int)


    def normalize(self):
        table = str.maketrans("", "", string.punctuation)
        for url, content in self.contents:
            words = [word.lower() for word in content.translate(table).split() if word.lower() not in self.stopwords]
            self.normalized_contents.append((url, words))

    def calculate_frequency_distribution(self, normalized_content):
        hist = defaultdict(int)

        for word in normalized_content:
            hist[word] += 1

        return hist

    def build_index(self):
        self.normalize()
        
        for url, content in self.normalized_contents:
            word_freq = self.calculate_frequency_distribution(content)

            for word, freq in word_freq.items():
                self.document_frequency[word] += 1
                self.term_frequency[word].append((url, freq))










