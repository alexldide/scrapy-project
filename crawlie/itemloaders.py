import scrapy
from itemloaders.processors import TakeFirst


class Take5Item(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    address = scrapy.Field()
    telephone = scrapy.Field()
    services = scrapy.Field()
    opening_hours = scrapy.Field()
    shop_url = scrapy.Field()


class RedFinItem(scrapy.Item):
    agent_id = scrapy.Field(output_processor=TakeFirst())
    full_name = scrapy.Field(output_processor=TakeFirst())
    phone_number = scrapy.Field(output_processor=TakeFirst())
