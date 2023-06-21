import scrapy
from ..items import NetbianItem


class BianSpider(scrapy.Spider):
    name = 'bian'
    # allowed_domains = ['netbian.com']
    start_urls = ['http://www.netbian.com/meinv/']

    def parse(self, response):
        group_urls = response.css('.list li a::attr(href)').extract()
        for group_url in group_urls:
            if not group_url.startswith("http"):
                group_url = response.urljoin(group_url)
                yield scrapy.Request(group_url, callback=self.parse_img_url)

        next_page = response.xpath('//div[@class="page"]/a[contains(.,"下一页")]/@href').get()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page)

    def parse_img_url(self, response):
        img_url = response.css('.pic img::attr(src)').get()
        yield scrapy.Request(img_url, callback=self.parse_img_content)

    def parse_img_content(self, response):
        filename = response.url.split('/')[-1]
        image_bytes = response.body
        yield NetbianItem(filename=filename, image_bytes=image_bytes)