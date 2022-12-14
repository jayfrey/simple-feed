from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from crawler.items import Article
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse


class FreeMalaysiaTodaySpider(CrawlSpider):
    name = "free_malaysia_today"
    allowed_domains = ["www.freemalaysiatoday.com"]
    start_urls = ["https://www.freemalaysiatoday.com/"]
    base_url = "https://www.freemalaysiatoday.com/"

    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"

    rules = [
        Rule(
            LinkExtractor(
                restrict_xpaths=".//div[@id='td_uid_8_5dc2b695b82d9']",
                attrs=["href"],
                tags=["a"],
            ),
            callback="parse_latest_articles",
            follow=True,
        ),
    ]

    def parse_latest_articles(self, response):
        item = Article()
        soup = BeautifulSoup(response.body, "lxml")
        header = soup.find("header", class_="td-post-title")
        content = soup.find("div", class_="td-post-content")

        item["title"] = header.find("h1", class_="entry-title").text
        item["article_image_url"] = content.find("img")["data-cfsrc"]
        item["published_date"] = header.find("time")["datetime"]
        item["publisher_name"] = (
            header.find("div", class_="td-post-author-name").find("a").text
        )
        item["article_content"] = "".join(
            map(str, content.find_all(["figure", "p"])[1:])
        )
        item["article_url"] = response.url
        item["topic"] = urlparse(response.url).path.split("/")[2]
        item["tags"] = ", ".join(
            [tag.text for tag in soup.find("ul", class_="td-tags").find_all("li")[1:]]
        )
        item["source"] = self.name

        yield item
