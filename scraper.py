import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    custom_settings = {
        'DUPEFILTER_DEBUG': True,
    }
    start_urls = ['https://en.wikipedia.org/wiki/Sweden']
    visited = [start_urls[0]]
    completed = []
    to_visit = []

    def parse(self, response):
        next_page = None
        links = response.css('div.mw-parser-output > p > a::attr(href)').extract()
        if len(links) == 0:
            self.set_visited(False)
        else:
            for link in links:
                if link.startswith("/wiki/") and len(link.split('/')) == 3 and len(link.split('#')) == 1:
                    if next_page is None:
                        next_page = link
                        new_start = True
                        if link == '/wiki/Philosophy':
                            self.set_visited(True)
                        elif link in self.visited:
                            self.set_visited(False)
                        elif self.in_completed(link):
                            self.set_visited(self.completed[self.in_completed(link)][1])
                        else:
                            self.visited.append(next_page)
                            #print(len(self.to_visit))
                            print('n')
                            yield response.follow(next_page, callback=self.parse)
                            new_start = False
                        if new_start:
                            print('s')
                            end = True
                            for i in range(len(self.to_visit)):
                                if not self.in_completed(self.to_visit[i]):
                                    self.visited.append(self.to_visit[i])
                                    next = self.to_visit.pop(i)
                                    # print('s')
                                    # print(len(self.to_visit))
                                    yield response.follow(next, callback=self.parse)
                                    end = False
                            # if end:
                            #     trues = 0
                            #     falses = 0
                            #     for i in range(len(self.completed)):
                            #         if self.completed[i][1] == True:
                            #             trues += 1
                            #         else:
                            #             falses += 1
                            #     print("{} and {}".format("Trues", trues))
                            #     print("{} and {}".format("Falses", falses))
                    elif link not in self.visited and not self.in_completed(link) and link not in self.to_visit:
                        self.to_visit.append(link)

    def set_visited(self, value):
        for i in range(len(self.visited)):
            self.completed.append((self.visited[i], value))
        self.visited = []

    def in_completed(self, link):
        for i in range(len(self.completed)):
            if link == self.completed[i][0]:
                return i
        return False
