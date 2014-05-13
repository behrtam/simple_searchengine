from crawler import Crawler
from page_rank import PageRank
from indexer import Indexer
from scorer import Scorer

from urllib.parse import urljoin


SEED_URL = 'http://mysql12.f4.htw-berlin.de/crawl/'
SEED_PAGES = ('d01.html', 'd06.html', 'd08.html')

STOP_WORDS = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',  
'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do'
'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
'that', 'the', 'this', 'to', 'we']


crawler = Crawler([urljoin(SEED_URL, page) for page in SEED_PAGES])

print("\n# Crawler TEST")

print("  total pages:  " + ("OK" if len(crawler.webgraph_out) == 8 else "WRONG"))

d01_outlinks = crawler.webgraph_out['http://mysql12.f4.htw-berlin.de/crawl/d01.html']
print("  d01 outlinks:  " + ("OK" if len(d01_outlinks) == 3 else "WRONG"))

d08_outlinks = crawler.webgraph_out['http://mysql12.f4.htw-berlin.de/crawl/d08.html']
print("  d08 outlinks:  " + ("OK" if len(d08_outlinks) == 0 else "WRONG"))



page_rank = PageRank(crawler.webgraph_in, crawler.webgraph_out)
page_rank.calculate_graph()

print("\n# PageRank TEST")

d08_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d08.html')
print("  d08 rank:  " + ("OK" if round(d08_rank, 4) == 0.0073 else "WRONG"))

d05_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d05.html')
print("  d05 rank:  " + ("OK" if round(d05_rank, 4) == 0.1173 else "WRONG"))

d02_rank = page_rank.get_rank('http://mysql12.f4.htw-berlin.de/crawl/d02.html')
print("  d02 rank:  " + ("OK" if round(d02_rank, 4) == 0.1254 else "WRONG"))


index = Indexer(crawler.contents, STOP_WORDS)
index.build_index()

print(index.documents_length())

scorer = Scorer(index.term_frequency, index.documents_length(), len(crawler.webgraph_out), STOP_WORDS)
for doc, score in scorer.calculate_scores('tokens').items():
	print(doc, score)
