# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MyItem(Item):
    """
    To store data to Postgres, always make sure your item classes inherit from MyItem and
    add "primary=True" metadata to Field, it's recommended that the primary field is unique in the table
    """

    def __init__(self):
        super().__init__()

    def sanitise_items(self):
        for k, v in self.deepcopy().items():
            if v == None:
                self.pop(k)
            else:
                if type(v) == list:
                    if not v:
                        self.pop(k)

                elif type(v) == str:
                    if v.strip() == "" or v.strip() == "–":
                        self.pop(k)

    def get_primary_fields(self):
        """
        This method returns primary field, otherwise, returns the first key in the item/dict
        """
        primary_fields = []
        for k in self.keys():
            if self.fields[k].get("primary", False):
                primary_fields.append(k)

        if primary_fields:
            return primary_fields
        else:
            return next(iter(self))


class Article(MyItem):
    title = Field(primary=True)
    image_url = Field()
    published_date = Field()
    publisher_name = Field()
    html_content = Field()
    page_url = Field()
    category_tags = Field()
    topic = Field()
    tags = Field()
    source = Field(primary=True)
