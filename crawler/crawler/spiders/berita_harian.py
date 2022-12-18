from scrapy.spiders import Spider, Request
from datetime import datetime, timedelta
from crawler.items import Article
from ..constants import DEFAULT_DATETIME_FORMAT
from twisted.internet import reactor, defer

import json
import urllib.parse


class BeritaHarianSpider(Spider):
    name = "berita_harian"
    table_name = "articles"
    allowed_domains = ["www.bharian.com.my"]
    start_urls = ["https://www.bharian.com.my/"]
    base_url = "https://www.bharian.com.my/"

    def parse(self, response):

        # Category ID
        # berita - 9206
        # sukan - 9207
        # dunia - 9208
        # hiburan - 9209
        # bisnes - 9210
        # rencana - 9211
        # wanita - 9212
        # hujung minggu - 9213
        category_ids = [str(int(str(i).zfill(3)) + 9200) for i in range(6, 14)]

        for category_id in category_ids:
            url = self.base_url + "api/collections/" + category_id + "?"
            params = {
                "page": "0",
                "page_size": "12",
            }

            yield Request(
                url + urllib.parse.urlencode(params),
                self.parse_latest_articles,
                dont_filter=True,
            )

    def parse_latest_articles(self, response):
        body_string = response.body.decode("utf-8")
        articles = json.loads(body_string)

        # The collections API from Berita Harian response is inconsistent,
        # very often latest articles are not returned out of the 8 requests
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
                item["topic"] = article["field_article_topic"]["name"]

                if article["field_tags"]:
                    item["tags"] = [tag["name"] for tag in article["field_tags"]]

                item["source"] = self.name

                yield item

    def deferred_parse_latest_articles(self, response):
        d = defer.Deferred()
        reactor.callLater(
            10,
            d.callback,
            Request(
                response.url,
                self.parse_latest_articles,
                dont_filter=True,
            ),
        )
        return d
