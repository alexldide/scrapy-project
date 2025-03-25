import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from crawlie.itemloaders import RedFinItem


class Redfin(scrapy.Spider):
    name = 'redfin'
    allowed_domains = ['redfin.com']
    start_urls = ['https://www.redfin.com/']

    def parse(self, response: Response, **kwargs):
        city_urls = response.xpath("//span[@class='city-list-title']/following-sibling::ul/li/a/@href").getall()
        for city in city_urls:
            agents_url = city + '/real-estate/agents'
            yield response.follow(url=agents_url, callback=self.parse_agents, priority=1)

    def parse_agents(self, response: Response):
        agents = response.xpath("//div[@class='agents']/div/a[1]/@href")
        yield from response.follow_all(urls=agents, callback=self.parse_agent_details)

    def parse_agent_details(self, response: Response):
        loader = ItemLoader(item=RedFinItem(), response=response)

        loader.add_xpath('full_name', "//div[@class='agent-name']/h1/text()")
        loader.add_xpath('agent_id', "//div[contains(.,'License')]/text()", re=r'\d+')
        loader.add_xpath('phone_number', "//div[@class='number']/a/text()")

        yield loader.load_item()
