# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import ArticleItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//section[@class='ouvJEz']/h1[@class='_1RuRku']/text()").get()
        author = response.xpath("//span/text()").getall()[3]
        content = response.xpath("//article[@class ='_2rhmJa']").getall()
        item = ArticleItem(
            title=title,
            author=author,
            content=content
        )
        yield item