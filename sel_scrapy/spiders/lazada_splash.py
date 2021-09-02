import scrapy
from scrapy_splash import SplashRequest

from sel_scrapy.items import LaptopItem


class LazadaSplashSpider(scrapy.Spider):
    name = 'lazada_splash'

    def start_requests(self):
        yield SplashRequest('https://www.lazada.com.ph/shop-laptops/')

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
