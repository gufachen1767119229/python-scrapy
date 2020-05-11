# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi#专门用来做数据处理
from pymysql import cursors

import pymysql
class JianshuPipeline(object):
    def __init__(self):
        dbparams = {
            'host':'localhost',
            'port':3306,
            'user':'root',
            'password':'root',
            'database':'jianshu',
            'charset':'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['author'],item['content']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,author,content)values(null,%s,%s,%s)
            """
            return self._sql
        return self._sql

# 使用scrapy自带的框架来实现异步爬取
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass':cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
               insert into article(id,title,author,content)values(null,%s,%s,%s)
               """
            return self._sql
        return self._sql

    def process_item(self,item,spider):
        deff = self.dbpool.runInteraction(self.insert_item,item)
        deff.addErrback(self.handle_error,item,spider)

    def insert_item(self,cursor,item):
        cursor.execute(self.sql,(item['title'],item['author'],item['content']))

    def handle_error(self,error,item,spider):
        print("="*10+"error"+"="*10)
        print(error)
        print("=" * 10 + "error" + "=" * 10)
