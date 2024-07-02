from typing import Any
import scrapy
from scrapy.http import Response
from ..items import QuoteItem

class Quote_spider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        items = QuoteItem()

        div_quotes = response.css("div.quote")
        
        for q in div_quotes:
            quote = q.css("span.text::text").extract()
            author = q.css("small.author::text").extract()
            tag = q.css("a.tag::text").extract()

            items["quote"] = quote
            items["author"] = author
            items["tag"] = tag

            yield items

        # Going to next page in sites with "next page" button
        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)