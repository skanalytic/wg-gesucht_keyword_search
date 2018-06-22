import datetime
import scrapy
from scrapy.crawler import CrawlerProcess
import os
from os.path import exists
import re

numbers = re.compile('\d+(?:\.\d+)?')

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

time = datetime.datetime.now()
start_url = ['https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.1.0.html?offer_filter=1&noDeact=1&city_id=8&category=2&rent_type=0&dFr=1531605600&dTo=1531605600']
output_json = 'wg_results.json'

# delete json
def delete_file(filename):
    if exists(filename):
        try:
            os.remove(filename)
        except OSError as ioe:
            print('File {0} remove has failed. Error: {1}'.format(filename, ioe))

delete_file(output_json)

class CoinMarketCapICOSpider(scrapy.Spider):
    name = 'CMC_ICO_crawler'
    allowed_domains = ['coinmarketcap.com']
    start_urls = start_url

    def parse(self, response):
        time = datetime.datetime.now()
        table = response.xpath('//div[@id="main_column"]')
        rows = table.xpath('//div[@class="panel panel-default  list-details-ad-border"]')
        for row in rows:
            dates = row.css('b::text').extract()
            if len(dates) == 3:
                ava_from = dates[0]
                ava_to = dates[1]
                online_since = dates[2]
            elif len(dates) == 2:
                ava_from = dates[0]
                ava_to = ''
                online_since = dates[1]
            yield {
                'url' : "https://www.wg-gesucht.de/" + str(row.css('a::attr(href)').extract_first()),
                'size' : float(numbers.findall(str(row.css('a::text').extract()[0]).split('|')[0].replace(' ',''))[0]),
                'price': float(numbers.findall(str(row.css('a::text').extract()[0]).split('|')[1].replace(' ', ''))[0]),
                'title': str(row.css('h3').css('a::text').extract_first()).strip(),
                'description': re.sub(' +',' ',str(row.css('p::text').extract_first()).strip()).replace("\n", " "),
                'avalible_from': str(ava_from).replace('Verfügbar:','').replace(' ','').strip(),
                'avalible_to': str(ava_to).replace(' ','').replace('-','').strip(),
                'online_since': online_since.replace('Online:','').replace(' ','').strip(),
            }


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': output_json
    })

    process.crawl(CoinMarketCapICOSpider)
    process.start() # the script will block here until the crawling is finished


import pandas as pd
pd.set_option('display.max_colwidth', -1)

df = pd.read_json(output_json)
print(df)
print(df['avalible_from'])

