from scrapy.spiders import Spider, Request
from datetime import datetime, timedelta
from crawler.items import Article
from ..constants import DEFAULT_DATETIME_FORMAT
from twisted.internet import reactor, defer
from crawler.utils.html_helper import normalise_text

import json
import urllib.parse

CATEGORIES = {
    "berita": "9206",
    "sukan": "9207",
    "dunia": "9208",
    "hiburan": "9209",
    "bisnes": "9210",
    "rencana": "9211",
    "wanita": "9212",
    "hujung minggu": "9213",
}


class BeritaHarianSpider(Spider):
    name = "berita_harian"
    table_name = "articles"
    allowed_domains = ["www.bharian.com.my"]
    start_urls = ["https://www.bharian.com.my/"]
    base_url = "https://www.bharian.com.my/"

    def parse(self, response):
        for category, category_id in CATEGORIES.items():
            url = self.base_url + "api/collections/" + category_id + "?"
            params = {
                "page": "0",
                "page_size": "12",
            }

            yield Request(
                url + urllib.parse.urlencode(params),
                self.parse_latest_articles,
                dont_filter=True,
                meta={
                    "category": category,
                },
            )

    def parse_latest_articles(self, response):
        body_string = response.body.decode("utf-8")
        articles = json.loads(body_string)

        # The collections API response is quite inconsistent, very often
        # latest articles are not returned out of the 8 requests
        # that was made to fetch the latest articles.
        #
        # In here, request will be deferred and retry later if articles
        # are not returned in the response. Otherwise, proceed to scrape
        if len(articles) == 1:
            print(f"Retry {response.url} later")
            yield Request(
                response.url,
                self.deferred_parse_latest_articles,
                dont_filter=True,
                meta={
                    "category": response.meta["category"],
                },
            )
        else:
            print(f"{response.url} - OK")
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

                topic = article["field_article_topic"]["name"]

                item["category_tags"] = [
                    response.meta["category"],
                    normalise_text(topic),
                ]
                item["topic"] = topic

                if article["field_tags"]:
                    item["tags"] = [tag["name"] for tag in article["field_tags"]]

                item["source"] = self.name

                yield item

    # Schedule to retry url that returned response with no articles in 10 seconds
    def deferred_parse_latest_articles(self, response):
        d = defer.Deferred()
        seconds = 10
        reactor.callLater(
            seconds,
            d.callback,
            Request(
                response.url,
                self.parse_latest_articles,
                dont_filter=True,
                meta={
                    "category": response.meta["category"],
                },
            ),
        )
        return d
