from scrapy.spiders import Spider, CrawlSpider, Rule
from datetime import datetime
from crawler.items import Article
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..constants import DEFAULT_DATETIME_FORMAT

import re


def filter_article_content(soup):
    filtered_article_content = []

    article_content = soup.find("div", class_="story-content").find_all(
        "div", class_="each-segment"
    )[1:]

    for segment in article_content:
        # Skip segment that contains div element with class containing "related-source"
        if not segment.find("div", "related-source"):
            for e in segment.find_all(["p", "img", "iframe"]):
                e_string = str(e)
                if e.name == "p":
                    if e.has_attr("class"):
                        if e["class"] == "img-caption":
                            pass
                    else:
                        if e.text:
                            filtered_article_content.append(e_string)

                if e.name == "img":
                    if e.has_attr("alt"):
                        filtered_article_content.append(e_string)

                if e.name == "iframe":
                    filtered_article_content.append(e_string)

    return filtered_article_content


class SaysSpider(CrawlSpider):
    name = "says"
    allowed_domains = ["says.com"]
    start_urls = ["http://says.com/my"]

    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths=".//ul[contains(@class, 'news-feed-items')]/li/div[1]",
                attrs=["href"],
                tags=["a"],
                allow_domains=allowed_domains,
            ),
            callback="parse_latest_articles",
            follow=True,
        ),
    ]

    def parse_latest_articles(self, response):
        item = Article()
        soup = BeautifulSoup(response.body, "lxml")
        article_meta = soup.find("div", class_="story-meta").find("p")

        item["title"] = soup.find("h1", class_="story-title").text
        item["article_image_url"] = re.search(
            "background-image:url\('(.+?)'\);",
            soup.find("div", class_="story-cover-image")["style"],
        )[1]
        item["published_date"] = datetime.strptime(
            article_meta.text.split("—")[1].strip(), "%d %b %Y, %I:%M %p"
        ).strftime(DEFAULT_DATETIME_FORMAT)
        item["publisher_name"] = article_meta.find("a").text
        item["html_article_content"] = "".join(filter_article_content(soup))
        item["article_url"] = response.url
        item["topic"] = urlparse(response.url).path.split("/")[2]
        item["tags"] = [
            tag.text[1:] for tag in soup.find_all("a", class_="story-hashtag")
        ]
        item["source"] = self.name

        yield item
