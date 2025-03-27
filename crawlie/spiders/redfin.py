import re
import scrapy
from scrapy.http import Response
from scrapy.loader import ItemLoader
from crawlie.itemloaders import RedFinItem
from crawlie.processors import RemoveRegex
from crawlie.save_to_csv import save_to_csv


class Redfin(scrapy.Spider):
    name = 'redfin'
    allowed_domains = ['redfin.com']
    start_urls = ['https://www.redfin.com']

    def parse(self, response: Response, **kwargs):
        city_urls = response.xpath("(//span[@class='city-list-title'])[1]/following-sibling::ul/li/a/@href").getall()
        for city in city_urls:
            agents_url = city + '/real-estate/agents'
            yield response.follow(url=agents_url, callback=self.parse_agents)

    def parse_agents(self, response: Response):
        no_agents = response.xpath("//span[@class='numberAgentsDisplayed']/span[2]/text()").re_first(r'\d+')
        no_agents = int(no_agents) if no_agents else 0
        agents_list = re.findall(r'profileUrl\\\":\\\"(\.*\\[\w\\-]+)', response.text)[:no_agents]
        for agent_url in agents_list:
            agent_url = self.start_urls[0] + re.sub(r'\\', '/', agent_url).replace('u002F', '')
            agent_url = re.sub(r'/$', '', agent_url)
            yield response.follow(url=agent_url, callback=self.parse_agent_details)

    def parse_agent_details(self, response: Response):
        loader = ItemLoader(item=RedFinItem(), response=response)

        loader.add_xpath('full_name', "//div[contains(@class,'agent-name')]/h1/text()")
        loader.add_xpath('agent_id', "//div[contains(.,'License')]/text()", re=r'\d+')
        loader.add_xpath('phone_number', "//div[@class='number']/a/text()", RemoveRegex(r'[^\d]'))

        item = loader.load_item()
        save_to_csv(item, 'redfin_data.csv')

        yield item
