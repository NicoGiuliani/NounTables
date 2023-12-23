import scrapy
from scrapy.crawler import CrawlerProcess
import json

class NounSpider(scrapy.Spider):
    name = 'noun_spider'

    def start_requests(self):
       yield scrapy.Request('https://api.verbix.com/conjugator/iv1/6153a464-b4f0-11ed-9ece-ee3761609078/1/75/175/m%C3%A6la')

    def parse(self, response):
        response_body = response.body.decode('utf-8')
        json_data = json.loads(response_body)

        html_content = json_data.get('p1').get('html')
        selector = scrapy.Selector(text=html_content)
        verbtable = selector.css('.verbtable .columns-main').get()

        yield { "verb": verbtable }

    def __init__(self, urls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_urls = urls


    def run_spider(self):
      process = CrawlerProcess(
        settings={
          'FEED_URI': 'C:/Users/ngiul/Documents/Github/NounTables/nountables/api/scrapy_output.json',
          'FEED_FORMAT': 'json',
        }
      )

      process.crawl(NounSpider, urls=['https://api.verbix.com/conjugator/iv1/6153a464-b4f0-11ed-9ece-ee3761609078/1/75/175/m%C3%A6la'])
      process.start()


