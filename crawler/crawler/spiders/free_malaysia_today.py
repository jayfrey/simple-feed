from scrapy.spiders import Spider, Request
from datetime import datetime
from crawler.items import Article
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..constants import DEFAULT_DATETIME_FORMAT


class FreeMalaysiaTodaySpider(Spider):
    name = "free_malaysia_today"
    table_name = "articles"
    allowed_domains = ["www.freemalaysiatoday.com"]
    start_urls = ["https://www.freemalaysiatoday.com/"]
    base_url = "https://www.freemalaysiatoday.com/"

    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"

    def parse(self, response):
        links = LinkExtractor(
            allow=r"(https:\/\/www.freemalaysiatoday.com\/category\/category)(.+?)+",
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[".//div[@id='td-header-menu']"],
            allow_domains=self.allowed_domains,
        ).extract_links(response)

        for link in links:
            yield Request(
                link.url,
                self.parse_category,
            )

    def parse_category(self, response):
        # LATEST
        links = LinkExtractor(
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[".//div[contains(@class, 'td-category-grid')]"],
            allow_domains=self.allowed_domains,
        ).extract_links(response)

        for link in links:
            yield Request(
                link.url,
                self.parse_article,
            )

        # MAIN
        links = LinkExtractor(
            attrs=["href"],
            tags=["a"],
            restrict_xpaths=[".//div[contains(@class, 'td-ss-main-content')]"],
            allow_domains=self.allowed_domains,
        ).extract_links(response)

        for link in links:
            yield Request(
                link.url,
                self.parse_article,
            )

    def parse_article(self, response):
        item = Article()
        soup = BeautifulSoup(response.body, "lxml")
        header = soup.find("header", class_="td-post-title")
        content = soup.find("div", class_="td-post-content")

        item["title"] = header.find("h1", class_="entry-title").text
        item["image_url"] = content.find("img")["data-cfsrc"]
        item["published_date"] = datetime.strptime(
            header.find("time")["datetime"], "%Y-%m-%dT%H:%M:%S%z"
        ).strftime(DEFAULT_DATETIME_FORMAT)
        item["publisher_name"] = (
            header.find("div", class_="td-post-author-name").find("a").text
        )
        item["html_content"] = "".join(map(str, content.find_all(["figure", "p"])[1:]))
        item["page_url"] = response.url
        item["topic"] = urlparse(response.url).path.split("/")[2]
        item["tags"] = [
            tag.text for tag in soup.find("ul", class_="td-tags").find_all("li")[1:]
        ]
        item["source"] = self.name

        yield item
