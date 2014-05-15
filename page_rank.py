def url_short(url):
    return url.split('/')[-1].split('.')[0]

class PageRank:
    def __init__(self, incoming_graph = None, outgoing_graph = None, damping_factor = .95, delta_threshold = 0.04):
        self.damping_factor = damping_factor
        self.delta_threshold = delta_threshold

        self.incoming_graph = incoming_graph
        self.outgoing_graph = outgoing_graph

        self.page_rank = {}

    @property
    def damping_factor(self):
        return self._damping_factor

    @damping_factor.setter
    def damping_factor(self, value):
        if not value or not (0 < value <= 1):
            raise Exception("damping factor cannot be empty, negative or greater than 1.0")
        self._damping_factor = value

    @property
    def delta_threshold(self):
        return self._delta_threshold

    @delta_threshold.setter
    def delta_threshold(self, value):
        if not value or value < 0:
            raise Exception("delta_threshold cannot be empty or negative")
        self._delta_threshold = value

    def get_rank(self, url):
        return None if not url in self.page_rank else self.page_rank[url]

    def build_graph(self):
        ''' Calculates the webgraph until the given delta threshold is met. '''
        self._init_step()
        run = True
        while run:
            run = self._next_step() > self.delta_threshold

    def _calculate_dangling_pages_part(self):
        part = 0
        for url, links in self.outgoing_graph.items():
            if not links:
                part += self.get_rank(url) / len(self.outgoing_graph)
        
        return part

    def _calculate_backlink_part(self, url):
        part = 0
            
        for backlink in self.incoming_graph[url]:
            part += self.get_rank(backlink) / len(self.outgoing_graph[backlink])
        
        return part

    def _init_step(self):
        N = len(self.outgoing_graph)

        for url in self.outgoing_graph.keys():
            self.page_rank[url] = 1 / N

    def _next_step(self):
        ''' Calculates the next iteration (step) of the webgraphs pageranks
            and returns the delta to the previous step. '''
        next_page_rank = {}
        
        tele_rate = 1.0 - self.damping_factor
        dangling_pages_part = self._calculate_dangling_pages_part()
        
        delta = 0

        for url in self.outgoing_graph:
            backlink_part = self._calculate_backlink_part(url)
            
            rank = self.damping_factor * (backlink_part + dangling_pages_part) 
            rank += (tele_rate / len(self.outgoing_graph))

            next_page_rank[url] = rank

            delta += abs(rank - self.get_rank(url))

        self.page_rank = next_page_rank

        return delta