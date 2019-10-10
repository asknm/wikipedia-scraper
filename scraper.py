import scrapy

class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    start_urls = ['https://en.wikipedia.org/wiki/Sweden']
    visited_links = [start_urls[0]]

    def parse(self, response):
        for link in response.css('div.mw-parser-output > p > a::attr(href)').extract():
            yield {
                'name': link,
            }
            break
