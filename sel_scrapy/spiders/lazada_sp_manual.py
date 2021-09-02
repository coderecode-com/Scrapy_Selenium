import json

import scrapy
from scrapy.http import Headers


class LazadaSpManualSpider(scrapy.Spider):
    name = 'lazada_sp_manual'

    def start_requests(self):
        req_url = "http://localhost:8050/render.json"
        url = 'https://www.lazada.com.ph/shop-laptops/'
        body = json.dumps({
            "url": url,
            "har": 1,
            "html": 0,
        })
        headers = Headers({'Content-Type': 'application/json'})
        yield scrapy.Request(req_url, method='POST', body=body, headers=headers)

    def parse(self, response, **kwargs):
        for link in response.xpath('//*[@data-qa-locator="product-item"]//a[text()]/@href').getall():
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_products)

    def parse_products(self, response, **kwargs):
        item = LaptopItem(
            name=response.css('.breadcrumb_item_anchor.breadcrumb_item_anchor_last ::text').get(),
            price=response.css('.pdp-price ::text').get()
        )

        yield item
