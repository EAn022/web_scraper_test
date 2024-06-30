from typing import Any
import scrapy
from scrapy.http import Response

class Quote_spider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        div_quotes = response.css("div.quote")
        
        for q in div_quotes:
            quote = q.css("span.text::text").extract()
            author = q.css("small.author::text").extract()
            tag = q.css("a.tag::text").extract()
            yield {
                "quote" : quote,
                "author" : author,
                "tag" : tag
            } 