from pathlib import Path

import scrapy 

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # def start_requests(self):
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]

        # optional: can be replaced with renaming urls into start_urls
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # code just to save response html sites
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        #extract data and save it into json file:
        for quote in response.css("div.quote"):
            yield{
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall()
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


 # in terminal run: scrapy shell url
 # then you can select elements from the response to extract data 
 # with: response.css("x").getall() ...
 # also you can use xpath: response.xpath("//title")

 # css selectors are converted to xpath expressions because it can look directly at the content