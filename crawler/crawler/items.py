# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Article(Item):
    title = Field()
    image_url = Field()
    published_date = Field()
    publisher_name = Field()
    html_content = Field()
    page_url = Field()
    topic = Field()
    tags = Field()
    source = Field()
