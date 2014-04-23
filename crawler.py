import requests
import string

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from collections import defaultdict

class Downloader:
    @staticmethod
    def get_page(url):
        # TODO: 200, 404, etc are handled but a timeout could be added
        response = requests.get(url)
        return response.content if response.status_code == requests.codes.ok else None

class Parser:
    def __init__(self, html, source_url):
        self.soup = BeautifulSoup(html)
        self.url = source_url

    def get_links(self):
        links = [urljoin(self.url, link.attrs['href']) for link in self.soup.find_all('a') if 'href' in link.attrs]
        return links

    def get_words(self):
        text = self.soup.body.get_text()
        # translate (which is faster than regex) is used to remove all punctuation
        table = str.maketrans("", "", string.punctuation)
        return text.translate(table).split()

class Frontier:
    def __init__(self, seed_urls):
        #TODO: validate urls
        self.visted_pages = []
        self.upcoming_pages = seed_urls

    def add_page(self, url):
        if not url in self.visted_pages and not url in self.upcoming_pages:
            self.upcoming_pages.append(url)

    def add_pages(self, urls):
        for url in urls:
            self.add_page(url)

    def has_next_page(self):
        return len(self.upcoming_pages) > 0

    def get_next_page(self):
        if not self.upcoming_pages: return None
        
        url = self.upcoming_pages.pop()
        self.visted_pages.append(url)
        return url


class Crawler:
    def __init__(self, seed_urls):
        self.webgraph_out = {}
        self.webgraph_in = defaultdict(list)

        self._crawl_pages(seed_urls)
        self._generate_ingraph()

    def _crawl_pages(self, seed_urls):
        front = Frontier(seed_urls)

        while front.has_next_page():
            next_url = front.get_next_page()
            p = Parser(Downloader.get_page(next_url), next_url)
            links = p.get_links()
            front.add_pages(links)

            self.webgraph_out[next_url] = tuple(links)

    def _generate_ingraph(self,):
        for url, links in self.webgraph_out.items():
            for link in links:
                self.webgraph_in[link].append(url)
