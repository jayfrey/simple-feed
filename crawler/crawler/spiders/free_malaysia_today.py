from scrapy.spiders import Spider, Request
from datetime import datetime
from crawler.items import Article
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..constants import DEFAULT_DATETIME_FORMAT
from crawler.utils.html_helper import normalise_text


class FreeMalaysiaTodaySpider(Spider):
    name = "free_malaysia_today"
    table_name = "articles"
    allowed_domains = ["www.freemalaysiatoday.com"]
    start_urls = ["https://www.freemalaysiatoday.com/"]
    base_url = "https://www.freemalaysiatoday.com/"

    user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"

    processed_url = dict()

    def parse(self, response):
        # Get and filter menu
        menus = response.xpath(".//ul[@id='menu-header-menu-1']/li")[0:9]

        for menu in menus:
            category = normalise_text(menu.xpath("a/text()").get())

            sub_menus = menu.xpath("ul[contains(@class, 'sub-menu')]/li")
            if sub_menus:
                for sub_menu in menu.xpath("ul[contains(@class, 'sub-menu')]/li"):
                    sub_category = normalise_text(sub_menu.xpath("a/text()").get())
                    sub_category_url = sub_menu.xpath("a/@href").get()

                    yield Request(
                        sub_category_url,
                        self.parse_category,
                        dont_filter=True,
                        meta={
                            "category_tags": [category, sub_category],
                        },
                    )
            else:
                category_url = normalise_text(menu.xpath("a/@href").get())
                yield Request(
                    category_url,
                    self.parse_category,
                    dont_filter=True,
                    meta={
                        "category_tags": [category],
                    },
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
                dont_filter=True,
                meta={
                    "category_tags": response.meta["category_tags"],
                },
            )

        # MAIN - uncomment to scrape articles from the main a.k.a bottom left section of the landing sub category page
        # links = LinkExtractor(
        #     attrs=["href"],
        #     tags=["a"],
        #     restrict_xpaths=[".//div[contains(@class, 'td-ss-main-content')]"],
        #     allow_domains=self.allowed_domains,
        # ).extract_links(response)

        # for link in links:
        #     yield Request(
        #         link.url,
        #         self.parse_article,
        #         dont_filter=True,
        #         meta={
        #             "category_tags": response.meta["category_tags"],
        #         },
        #     )

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
        item["category_tags"] = response.meta["category_tags"]
        item["topic"] = urlparse(response.url).path.split("/")[2]
        item["tags"] = [
            tag.text for tag in soup.find("ul", class_="td-tags").find_all("li")[1:]
        ]
        item["source"] = self.name

        # The following block will combine all the relevant categories related to an article
        # This happens when an article is tagged on two different categories, e.g. tech and automobile
        if response.url in self.processed_url.keys():
            category_tags = response.meta["category_tags"].copy()
            category_tags.extend(self.processed_url[response.url]["category_tags"])
            item["category_tags"] = list(set(category_tags))

        self.processed_url[response.url] = item

        yield item
