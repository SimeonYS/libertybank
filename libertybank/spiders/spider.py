import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import LlibertybankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class LlibertybankSpider(scrapy.Spider):
	name = 'libertybank'
	start_urls = ['https://www.libertybank.net/about/news.cfm#']

	def parse(self, response):
		post_links = response.xpath('//div[@class="featuresbox"]/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Not stated in article"
		title = response.xpath('//div[@class="column-left"]/h2/text()').get()
		content = response.xpath('//div[@class="column-left"]//text()[not (ancestor::h2 or ancestor::a[@class="cta"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=LlibertybankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
