# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        #如果需要爬取点击展开更多专题，就需要点击按钮，并且判断是否还有更多专题，如果没有，就报错pass掉
        # 然后在settings里面打开DOWNLOAD
        # try:
        #     while True:
        #         showmore = self.driver.find_element_by_class_name('***')
        #         showmore.click()
        #         time.sleep(0.1)
        #         if not showmore:
        #             break
        # except:
        #     pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request)
        return response