import scrapy
from itemloaders.processors import TakeFirst


class Take5Item(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    latitude = scrapy.Field(output_processor=TakeFirst())
    longitude = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst())
    telephone = scrapy.Field()
    services = scrapy.Field()
    opening_hours = scrapy.Field()
    shop_url = scrapy.Field(output_processor=TakeFirst())
    first_open_date = scrapy.Field(output_processor=TakeFirst())


class RedFinItem(scrapy.Item):
    agent_id = scrapy.Field(output_processor=TakeFirst())
    full_name = scrapy.Field(output_processor=TakeFirst())
    phone_number = scrapy.Field(output_processor=TakeFirst())
