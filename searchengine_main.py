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

page_rank = PageRank(crawler.webgraph_in, crawler.webgraph_out)
page_rank.build_graph()

index = Indexer(crawler.contents, STOP_WORDS)
index.build_index()

scorer = Scorer(index)

print("> SIMPLE SEARCH ENGINE (by Tammo, Tim & Flo)")

while True:
    scores = scorer.calculate_scores(input("\n> query: "))

    if not scores:
        print("your search term does not occur on any page")
        continue

    ranked_scores = [(url, score, page_rank.get_rank(url), score * page_rank.get_rank(url)) for url, score in scores.items()]
    
    print("\n               url | score  | rank   | rank * score\n" + "-" * 54)
    for url, score, rank, ranked_score in sorted(ranked_scores, key=lambda element: element[3], reverse=True):
        print(" ..{} | {:.4f} | {:.4f} | {:.4f}".format(url[-15:], round(score, 6), round(rank, 6), round(ranked_score, 6)))
