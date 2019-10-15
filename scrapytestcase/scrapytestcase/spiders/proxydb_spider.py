import scrapy
import json
import re
import base64

class ProxydbSpider(scrapy.Spider):
    name = 'proxydb'
    start_urls = [
        'http://proxydb.net/?country=&page=1'
    ]


    def parse(self, response):
        self.response = response

        data = []
        for el in response.css('tbody tr td script').extract():
            data.append({
                'ip_address': self.get_ip_address(el),
                'port': self.get_port(el)
            })

        with open('items.json', 'w') as outfile:
            json.dump(data, outfile)

    def get_ip_address(self, el):
        """Get ip_address from html element"""
        ip_address_part_one = re.findall(r"'((\d*)+\.\d+\.\d*)'", el.split("\n")[2])[0][0][::-1]
        ip_address_part_two = base64.b64decode(re.findall(r"\('(.*?)'.", el.split("\n")[3])[0].encode().decode('unicode-escape')).decode(encoding="utf-8")
        return ip_address_part_one + ip_address_part_two

    def get_port(self, el):
        """Get port from html element"""
        port_part_one = int(re.findall(r'"(.*?)"', self.response.xpath('//div').re_first(r'data-rnn.+?"\d+"'))[0])
        port_first_two = int(re.findall(r'\d+', el.split("\n")[4])[0])
        return port_part_one + port_first_two
