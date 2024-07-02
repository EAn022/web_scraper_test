from typing import Any
import scrapy
from scrapy.http import Response
from scrapy.http import FormRequest
from ..items import QuoteItem

class Quote_spider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        token = response.css("form input::attr(value)").extract_first()
        return FormRequest.from_response(response, formdata = {
                                                                "csrf" : token,
                                                                "username" : "abc@aaa.com",
                                                                "password" : "123abc"
        }, callback = self.start_scraping)
    
    def start_scraping(self, response):
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