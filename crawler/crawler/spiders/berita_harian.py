from scrapy.spiders import Spider, Request
from datetime import datetime, timedelta
from crawler.items import Article
from ..constants import DEFAULT_DATETIME_FORMAT

import json
import urllib.parse


class BeritaHarianSpider(Spider):
    name = "berita_harian"
    allowed_domains = ["www.bharian.com.my"]
    start_urls = ["https://www.bharian.com.my/"]
    base_url = "https://www.bharian.com.my/"

    def parse(self, response):
        url = self.base_url + "api/articles?"
        params = {
            "sttl": "true",
            "page_size": "8",
        }
        yield Request(
            url + urllib.parse.urlencode(params),
            self.parse_latest_articles,
        )

    def parse_latest_articles(self, response):
        body_string = response.body.decode("utf-8")
        articles = json.loads(body_string)

        for article in articles:
            item = Article()

            item["title"] = article["title"]
            item["image_url"] = article["field_article_images"][0]["url"]

            item["published_date"] = (
                datetime.fromtimestamp(article["created"]) + timedelta(hours=8)
            ).strftime(DEFAULT_DATETIME_FORMAT)

            if article["field_article_author"]:
                item["publisher_name"] = article["field_article_author"]["name"]

            item["html_content"] = article["body"]
            item["page_url"] = article["url"]
            item["topic"] = article["field_article_topic"]["name"]

            if article["field_tags"]:
                item["tags"] = [tag["name"] for tag in article["field_tags"]]

            item["source"] = self.name

            yield item
