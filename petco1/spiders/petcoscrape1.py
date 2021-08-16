import scrapy
import json
import requests
from lxml import html
from ..items import Petco1Item

class Petcoscrape1Spider(scrapy.Spider):
    name = 'petcoscrape1'
    # allowed_domains = ['petco.com']
    # start_urls = ['http://petco.com/']

    def start_requests(self):
        url = r'https://maps.stores.petco.com/api/getAsyncLocations?template=search&level=search&search=10010&radius=100'
        yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        items = Petco1Item()
        json_response = response.json()
        # print(json_response['markers'])
        for i in json_response.get('markers',[]):

            def storetiming(url1):
                r = requests.get(url1)
                html_response1 = html.fromstring(r.content)
                time = ['Monday : ','Tuesday : ','Wednesday : ','Thursday : ','Friday : ','Saturday : ','Sunday : ']
                open = html_response1.xpath('//span[@class="time-open"]/text()')
                close = html_response1.xpath('//span[@class="time-close"]/text()')
                for i in range(7):
                    time[i] = time[i] + open[i] + ' - ' + close[i]
                return time

            info = i.get('info','')
            info.replace('\\','')
            html_response = html.fromstring(info)
            dict_1 = html_response.xpath('//div[@class="tlsmap_popup"]/text()')[0]
            string_dict = ''.join(str(x) for x in dict_1)
            final_dict = json.loads(string_dict)
            url1 = final_dict.get('url', '')
            # print(final_dict)
            storetimings = storetiming(url1)

            items = {
                'StoreID':final_dict.get('fid', ''), 
                'StoreName':final_dict.get('location_name', ''), 
                'Street':final_dict.get('address_1', ''), 
                'City':final_dict.get('city', ''), 
                'State':final_dict.get('region', ''), 
                'StoreTiminings': ' | '.join(storetimings),
                'Phone': final_dict.get('local_phone', ''),
                'PostCode' : final_dict.get('post_code', ''),
                'StoreURL' : url1,
                'Latitude': final_dict.get('lat', ''),
                'Longitude': final_dict.get('lng', '')
            }
            yield items
