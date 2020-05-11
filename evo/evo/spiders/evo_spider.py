# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from evo.items import EvoItem

class EvoSpiderSpider(CrawlSpider):
    name = 'evo_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/3277.html']

    rules = (
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/3277.+"),callback="parse_page",follow=True),
    )


    def parse_page(self, response):
        category = response.xpath("//div[@class='uibox']/div/text()").get()
        #因为包含图片的class有很多个属性，所以使用contains来写
        srcs = response.xpath('//div[contains(@class,"uibox-con")]/ul/li//img/@src').getall()
        #将缩略原图的一部分URL元素替换，之后就可以变成高清的图片URL
        srcs = list(map(lambda x:x.replace("240x180_0_q95_c42","1024x0_1_q95"),srcs))
        # urls = []
        # for src in srcs:
        #     url = response.urljoin(src)
        #     urls.append(url)
        srcs = list(map(lambda x:response.urljoin(x),srcs))
        yield EvoItem(category=category,image_urls=srcs)


