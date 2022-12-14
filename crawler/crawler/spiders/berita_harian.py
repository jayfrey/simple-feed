from scrapy.spiders import Spider, Request
from datetime import datetime
from crawler.items import Article

import json


class BeritaHarianSpider(Spider):
    name = "berita_harian"
    allowed_domains = ["www.bharian.com.my"]
    start_urls = ["https://www.bharian.com.my/"]
    base_url = "https://www.bharian.com.my/"

    def parse(self, response):
        yield Request(
            "https://www.bharian.com.my/api/articles?sttl=true&page_size=8",
            self.parse_latest_articles,
        )

    def parse_latest_articles(self, response):
        body_string = response.body.decode("utf-8")
        articles = json.loads(body_string)

        for article in articles:
            item = Article()

            item["title"] = article["title"]
            item["article_image_url"] = article["field_article_images"][0]["url"]
            item["published_date"] = datetime.fromtimestamp(article["created"])

            if article["field_article_author"]:
                item["publisher_name"] = article["field_article_author"]["name"]

            item["article_content"] = article["body"]
            item["article_url"] = article["url"]
            item["topic"] = article["field_article_topic"]["name"]

            if article["field_tags"]:
                item["tags"] = ", ".join([tag["name"] for tag in article["field_tags"]])

            item["source"] = self.name

            yield item
