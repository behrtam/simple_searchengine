from crawler import Crawler
from page_rank import PageRank
from indexer import Indexer
from scorer import Scorer

from urllib.parse import urljoin
from pprint import pprint


SEED_URL = 'http://mysql12.f4.htw-berlin.de/crawl/'
SEED_PAGES = ('d01.html', 'd06.html', 'd08.html')

STOP_WORDS = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',  
'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
'that', 'the', 'this', 'to', 'we']


crawler = Crawler([urljoin(SEED_URL, page) for page in SEED_PAGES])

print("\n# Crawler TEST")

print("  total pages:  " + ("OK" if len(crawler.webgraph_out) == 8 else "WRONG"))

d01_outlinks = crawler.webgraph_out['http://mysql12.f4.htw-berlin.de/crawl/d01.html']
print("  d01 outlinks:  " + ("OK" if len(d01_outlinks) == 3 else "WRONG"))

d04_outlinks = crawler.webgraph_out['http://mysql12.f4.htw-berlin.de/crawl/d04.html']
print("  d04 outlinks:  " + ("OK" if len(d04_outlinks) == 4 else "WRONG"))

d08_outlinks = crawler.webgraph_out['http://mysql12.f4.htw-berlin.de/crawl/d08.html']
print("  d08 outlinks:  " + ("OK" if len(d08_outlinks) == 0 else "WRONG"))



page_rank = PageRank(crawler.webgraph_in, crawler.webgraph_out)
page_rank.build_graph()

print("\n# PageRank TEST")

d08_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d08.html')
print("  d08 rank:  " + ("OK" if round(d08_rank, 4) == 0.0073 else "WRONG"))

d05_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d05.html')
print("  d05 rank:  " + ("OK" if round(d05_rank, 4) == 0.1173 else "WRONG"))

d02_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d02.html')
print("  d02 rank:  " + ("OK" if round(d02_rank, 4) == 0.1254 else "WRONG"))


index = Indexer(crawler.contents, STOP_WORDS)
index.build_index()

print("\n# Indexer TEST [tf df]")

# (classification, df:3) -> [('d06', 1), ('d08', 4), ('d07', 1)]
term1 = index.term_frequency['classification']
term1_checked = 0
for url, tf in term1:
    if 'd06' in url and (tf == 1): term1_checked += 1
    elif 'd08' in url and (tf == 4): term1_checked += 1
    elif 'd07' in url and (tf == 1): term1_checked += 1
    else: term1_checked += 1
print("  'classification' index:  " + ("OK" if term1_checked == 3 else "WRONG"))

# (index, df:3) -> [('d08', 4), ('d04', 1), ('d05', 2)]
term2 = index.term_frequency['index']
term2_checked = 0
for url, tf in term2:
    if 'd04' in url and (tf == 1): term2_checked += 1
    elif 'd08' in url and (tf == 4): term2_checked += 1
    elif 'd05' in url and (tf == 2): term2_checked += 1
    else: term2_checked += 1
print("  'index' index:  " + ("OK" if term2_checked == 3 else "WRONG"))

# (tokens, df:5) -> [('d01', 1), ('d08', 4), ('d02', 2), ('d03', 1), ('d04', 2)]
term3 = index.term_frequency['tokens']
term3_checked = 0
for url, tf in term3:
    if 'd01' in url and (tf == 1): term3_checked += 1
    elif 'd08' in url and (tf == 4): term3_checked += 1
    elif 'd02' in url and (tf == 2): term3_checked += 1
    elif 'd03' in url and (tf == 1): term3_checked += 1
    elif 'd04' in url and (tf == 2): term3_checked += 1
    else: term3_checked += 1
print("  'tokens' index:  " + ("OK" if term3_checked == 5 else "WRONG"))

print("\n# Indexer TEST [doc length]")

d08_len = index.documents_length['http://mysql12.f4.htw-berlin.de/crawl/d08.html']
print("  d08 length:  " + ("OK" if round(d08_len, 6) == 2.727447 else "WRONG"))

d06_len = index.documents_length['http://mysql12.f4.htw-berlin.de/crawl/d06.html']
print("  d06 length:  " + ("OK" if round(d06_len, 6) == 1.974093 else "WRONG"))

d04_len = index.documents_length['http://mysql12.f4.htw-berlin.de/crawl/d04.html']
print("  d04 length:  " + ("OK" if round(d04_len, 6) == 4.312757 else "WRONG"))


print("\n# Scorer TEST")

scorer = Scorer(index)

tokens_scores = scorer.calculate_scores('tokens')
tokens_scores_check = all(
    ((round(tokens_scores['http://mysql12.f4.htw-berlin.de/crawl/d08.html'], 6) == 0.119897),
     (round(tokens_scores['http://mysql12.f4.htw-berlin.de/crawl/d02.html'], 6) == 0.093106),
     (round(tokens_scores['http://mysql12.f4.htw-berlin.de/crawl/d04.html'], 6) == 0.061577),
     (round(tokens_scores['http://mysql12.f4.htw-berlin.de/crawl/d01.html'], 6) == 0.051784),
     (round(tokens_scores['http://mysql12.f4.htw-berlin.de/crawl/d03.html'], 6) == 0.045677)))
print("  'tokens' score:  " + ("OK" if tokens_scores_check else "WRONG"))

index_scores = scorer.calculate_scores('index')
index_scores_check = all(
    ((round(index_scores['http://mysql12.f4.htw-berlin.de/crawl/d08.html'], 6) == 0.250207),
     (round(index_scores['http://mysql12.f4.htw-berlin.de/crawl/d05.html'], 6) == 0.233073),
     (round(index_scores['http://mysql12.f4.htw-berlin.de/crawl/d04.html'], 6) == 0.098769)))
print("  'index' score:  " + ("OK" if index_scores_check else "WRONG"))

classification_scores = scorer.calculate_scores('classification')
classification_scores_check = all(
    ((round(classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d08.html'], 6) == 0.250207),
     (round(classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d06.html'], 6) == 0.215779),
     (round(classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d07.html'], 6) == 0.142045)))
print("  'classification' score:  " + ("OK" if classification_scores_check else "WRONG"))

tokens_classification_scores = scorer.calculate_scores('tokens classification')
tokens_classification_scores_check = all(
    ((round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d08.html'], 6) == 0.277451),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d06.html'], 6) == 0.194592),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d07.html'], 6) == 0.128098),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d02.html'], 6) == 0.040235),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d04.html'], 6) == 0.026610),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d01.html'], 6) == 0.022378),
     (round(tokens_classification_scores['http://mysql12.f4.htw-berlin.de/crawl/d03.html'], 6) == 0.019739)))
print("  'tokens classification' score:  " + ("OK" if tokens_classification_scores_check else "WRONG"))