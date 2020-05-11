# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from evo import settings

class EvoPipeline(object):
    def __init__(self):
        #判断文件夹EVO下面有没有图片存储文件夹（IMAGE）,如果没有就创建一个文件夹
        #1.s.path.dirname(__file__)方法可以获取Pipelines的目录即第二个EVO目录
        #2.os.path.dirname(os.path.dirname(__file__))方法可以获取第一个EVO的路径，即F:/untitled/scrapy_demon/EVO路径
        #3. os.path.join拼接出images的路径
        #4.判断是否存在images文件夹，如果没有存在就创建一个images文件夹
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)


    def process_item(self, item, spider):
        # 获取图片的类别，保存图片的时候按照类图片类别保存
        category = item['category']
        urls = item['urls']

        category_path = os.path.join(self.path, category)  # 判断images文件夹下面是否有categary文件夹
        if not os.path.exists(category_path):
            os.mkdir(category_path)

        for url in urls:
            # print(url[0])
            # print('-'*30)
            image_name = url.split("_")[-1]  # 将URL分割为图片存储的名字
            request.urlretrieve(url, os.path.join(category_path, image_name))
        return item


class EVOImagsPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #这个方法是在发送下载请求之前调用
        # 其实这个方法本身就是发送下载请求的
        request_objs = super(EVOImagsPipeline,self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        #这个方法是图片将要别存储的时候调用，来获取这个图片存储的路径
        path = super(EVOImagsPipeline,self).file_path(request,response,info)
        category = request.item.get('category')
        images_store = settings.IMAGES_STORE
        category_path = os.path.join(images_store,category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace("full/","")
        image_path = os.path.join(category_path,image_name)
        return image_path
