import json
import re
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader
from crawlie.itemloaders import Take5Item
from crawlie.processors import RemoveRegex
from crawlie.save_to_csv import save_to_csv


class Take5(SitemapSpider):
    name = 'take5'
    sitemap_urls = ['https://www.take5.com/sitemap.xml']
    sitemap_rules = [(r'/locations/.*/\d+/$', 'parse_location')]

    def parse_location(self, response):
        jmes = response.xpath("//script[contains(.,'latitude')]/text()").get()
        data = json.loads(jmes)

        loader = ItemLoader(item=Take5Item(), response=response)

        loader.add_value('id', re.findall(r'\d{3,}', response.url)[0])
        loader.add_value('latitude', data.get('geo')['latitude'])
        loader.add_value('longitude', data.get('geo')['longitude'])
        loader.add_value('address', ", ".join(list(data.get('address').values())[1:]))
        loader.add_value('telephone', data.get('telephone'), RemoveRegex(r'[^\d]'))
        loader.add_value('opening_hours', data.get('openingHours'))
        loader.add_value('shop_url', data.get('url'))

        loader.add_xpath('services', "//h4[contains(.,'Location Services')]/following-sibling::div//span/text()")
        loader.add_xpath('name', "normalize-space(//h1/text())", RemoveRegex(r'-.*'))
        loader.add_xpath('first_open_date', "//script[contains(.,'firstOpen')]/text()",
                         re=r'firstOpenDate\\\":\\\"(\d{2}/\d{2}/\d{4})')

        item = loader.load_item()
        save_to_csv(item, 'take5_data.csv')

        yield item
