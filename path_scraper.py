import scrapy
import random


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    custom_settings = {
        'DUPEFILTER_DEBUG': True,
    }
    file = open("to_visit.txt", "r")
    lines = file.readlines()
    start = random.choice(lines).split('\n')[0]
    start_urls = ["https://en.wikipedia.org" + start]
    visited = [start]

    def parse(self, response):
        #ps = response.css('div.mw-parser-output > pre').extract()
        ps = response.css('div.mw-parser-output > p').extract()
        in_parentheses = 0
        link = None
        done = False
        for p in ps:
            for word in p.split():
                in_parentheses += len(word.split('(')) - 1
                in_parentheses -= len(word.split(')')) - 1
                in_parentheses += len(word.split('[')) - 1
                in_parentheses -= len(word.split(']')) - 1
                if in_parentheses == 0 and word.startswith('href='):
                    link = word.split('"')[-2]
                    if link.startswith("/wiki/") and len(link.split('/')) == 3 and '#' not in link \
                            and not link == '/wiki/Geographic_coordinate_system':
                        done = True
                        break
                    else:
                        link = None
            if done:
                break
        print(link)
        if link is None:
            self.set_visited(False)
        elif link == '/wiki/Philosophy':
            self.visited.append(link)
            self.set_visited(True)
        elif link in self.visited:
            print(self.visited)
            self.visited.append(link)
            self.set_visited(False)
        elif self.in_completed(link) > -1:
            self.visited.append(link)
            index = self.in_completed(link)
            value = ""
            with open("completed_with_path.txt") as fp:
                for i, line in enumerate(fp):
                    if i == index:
                        value = line.split()[-1]
                    elif i > index:
                        break
            if value == "True":
                self.set_visited(True)
            elif value == "False":
                self.set_visited(False)
            else:
                print("SOMETHING WENT WRONG!")
        else:
            self.visited.append(link)
            yield response.follow(link, callback=self.parse)
            return

        file = open("to_visit.txt", "r")
        for line in file:
            if self.in_completed(line) == -1:
                next = line[:-1]
                self.visited.append(next)
                # print('s')
                # print(len(self.to_visit))
                yield response.follow(next, callback=self.parse)
                break


    def set_visited(self, value):
        file = open("completed_with_path.txt", "a")
        for i in range(len(self.visited)):
            file.write(self.visited[i] + " " + str(self.visited) + " " + str(value) + "\n")
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
        file = open("completed_with_path.txt", "r")
        i = 0
        for line in file:
            if line.startswith(link):
                return i
            i += 1
        return -1
