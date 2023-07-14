import scrapy
import re
from ..items import DimtownItem


class CosplaySpider(scrapy.Spider):
    name = 'cosplay'
    # allowed_domains = ['dimtown.com']
    start_urls = ['https://dimtown.com/cosplay']

    def parse(self, response):
        group_urls = response.css('#index_ajax_list li .kzpost-data>a::attr(href)').extract()
        for group_url in group_urls:
            yield scrapy.Request(group_url, headers=response.request.headers, callback=self.parse_img_url)

        # 获取下一页
        next_page = response.css('.nav-links a.next::attr(href)').get()
        if next_page:
            page_num = re.search(r'\d', next_page).group()
            yield scrapy.Request(next_page, headers=response.request.headers)

    def parse_img_url(self, response):
        name = response.css('.hx h1::text').get()
        name = re.sub(r'[\/:*?"<>|]', '', name)  #去除非法字符\/:*?"<>|
        img_urls = response.css('.content_left img::attr(src)').extract()
        for i, src in enumerate(img_urls, 1):
            yield scrapy.Request(src,
                                 callback=self.parse_img_content,
                                 meta={'name': f'{name}_{i}.jpg'})

    def parse_img_content(self, response):
        name = response.meta.get('name')
        image_bytes = response.body
        yield DimtownItem(name=name, image_bytes=image_bytes)