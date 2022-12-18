from scrapy.spiders import Spider, Request
from datetime import datetime
from crawler.items import Article
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..constants import DEFAULT_DATETIME_FORMAT
from crawler.utils.html_helper import normalise_text

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


class SaysSpider(Spider):
    name = "says"
    table_name = "articles"
    allowed_domains = ["says.com"]
    start_urls = ["http://says.com/my"]

    def parse(self, response):
        links = LinkExtractor(
            allow=r"(https:\/\/says.com\/my)(.+?)+",
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[
                ".//ul[contains(@class, 'channels')]/*/a[contains(@class, 'ga-channel')]",
                ".//ul[contains(@class, 'channels')]/*/*/a[contains(@class, 'ga-channel')]",
            ],
            allow_domains=self.allowed_domains,
        ).extract_links(response)

        for link in links:
            category = normalise_text(link.text)
            yield Request(
                link.url,
                self.parse_category,
                meta={
                    "category_tags": [category],
                },
            )

    def parse_category(self, response):
        # LATEST TOP
        links = LinkExtractor(
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[
                ".//div[@class='channel-story-info']/h3",
            ],
            allow_domains=self.allowed_domains,
        ).extract_links(response)
        for link in links:
            yield Request(
                link.url,
                self.parse_article,
                meta={
                    "category_tags": response.meta["category_tags"],
                },
            )

        # LATEST MAIN
        links = LinkExtractor(
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[
                ".//ul[contains(@class, 'news-feed-items')]/*/div[contains(@class, 'story-info')]/h3",
            ],
            allow_domains=self.allowed_domains,
        ).extract_links(response)
        for link in links:
            yield Request(
                link.url,
                self.parse_article,
                meta={
                    "category_tags": response.meta["category_tags"],
                },
            )

    def parse_article(self, response):

        # Some requests will redirect to "exclusive.says.com"
        # or says.com/my/exclusive, which is irrelevant and not an article
        if not (
            re.search(r"(https:\/\/exclusive.says.com\/my)(.+?)+", response.url)
            or re.search(r"(https:\/\/says.com\/my\/exclusive)(.+?)+", response.url)
        ):
            item = Article()
            soup = BeautifulSoup(response.body, "lxml")

            item["title"] = soup.find("h1", class_="story-title").text
            item["image_url"] = re.search(
                "background-image:url\('(.+?)'\);",
                soup.find("div", class_="story-cover-image")["style"],
            )[1]

            article_meta = soup.find("div", class_="story-meta").find("p")
            published_date = article_meta.contents[2].strip()[2:23]

            if published_date:
                item["published_date"] = datetime.strptime(
                    published_date, "%d %b %Y, %I:%M %p"
                ).strftime(DEFAULT_DATETIME_FORMAT)
            item["publisher_name"] = article_meta.find("a").text

            item["html_content"] = "".join(filter_article_content(soup))
            item["page_url"] = response.url
            item["category_tags"] = response.meta["category_tags"]
            item["topic"] = urlparse(response.url).path.split("/")[2]
            item["tags"] = [
                tag.text[1:] for tag in soup.find_all("a", class_="story-hashtag")
            ]
            item["source"] = self.name

            yield item
