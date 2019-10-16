import scrapy


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    custom_settings = {
        'DUPEFILTER_DEBUG': True,
    }
    file = open("to_visit.txt", "r")
    start = file.readline().split('\n')[0]
    start_urls = ["https://en.wikipedia.org" + start]
    visited = [start]

    def parse(self, response):
        next_page = None
        new_start = True
        links = response.css('div.mw-parser-output > p > a::attr(href)').extract()
        if len(links) == 0:
            print("NO MORE!")
            self.set_visited(False)
        else:
            for link in links:
                if link.startswith("/wiki/") and len(link.split('/')) == 3 and len(link.split('#')) == 1:
                    if next_page is None:
                        next_page = link
                        if link == '/wiki/Philosophy':
                            self.set_visited(True)
                        elif link in self.visited:
                            self.set_visited(False)
                        elif self.in_completed(link) > -1:
                            index = self.in_completed(link)
                            value = ""
                            with open("completed.txt") as fp:
                                for i, line in enumerate(fp):
                                    if i == index:
                                        value = line.split()[1]
                                    elif i > index:
                                        break
                            if value == "True":
                                self.set_visited(True)
                            elif value == "False":
                                self.set_visited(False)
                            else:
                                print("SOMETHING WENT WRONG!")
                        else:
                            self.visited.append(next_page)
                            yield response.follow(next_page, callback=self.parse)
                            new_start = False
                    elif link not in self.visited and self.in_completed(link) == -1 and not self.in_to_visit(link):
                        file = open("to_visit.txt", "a")
                        file.write(link + "\n")
                        file.close()
        if new_start:
            # print('s')
            file = open("to_visit.txt", "r")
            for line in file:
                if self.in_completed(line) == -1:
                    next = line[:-1]
                    self.visited.append(next)
                    # print('s')
                    # print(len(self.to_visit))
                    yield response.follow(next, callback=self.parse)
                    break

    def in_to_visit(self, link):
        file = open("to_visit.txt", "r")
        i = 0
        for line in file:
            if line.startswith(link):
                return True
            i += 1
        return False

    def set_visited(self, value):
        file = open("completed.txt", "a")
        for i in range(len(self.visited)):
            file.write(self.visited[i] + " " + str(value) + "\n")
        file.close()
        file = open("to_visit.txt", "r")
        to_visit = file.readlines()
        file.close()
        for v in self.visited:
            for line in to_visit:
                if line.startswith(v):
                    to_visit.remove(line)
        file = open("to_visit.txt", "w")
        file.writelines(to_visit)
        file.close()
        self.visited = []

    def in_completed(self, link):
        file = open("completed.txt", "r")
        i = 0
        for line in file:
            if line.startswith(link):
                return i
            i += 1
        return -1

