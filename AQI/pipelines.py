# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import redis
from pymongo import MongoClient
from scrapy.exporters import JsonItemExporter, CsvItemExporter

from AQI.items import AqiItem
import json


# 1.数据源管道  记录爬虫爬去数据的时间  和 爬虫的名字
class AqiDataPipeline(object):
    def process_item(self, item, spider):
        item['data_time'] = str(datetime.utcnow())  # 格林威治时间的当前时间
        item['spider'] = spider.name

        return item


# 2. json管道
class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('AQI.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, AqiItem):
            self.file.write(json.dumps(dict(item), ensure_ascii=False, indent=2) + ',\n')

        return item

    def close_spider(self, spider):
        self.file.close()


# 3. csv管道
class AqiCsvPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.csv', 'wb')
        # 写入器
        self.writer = CsvItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()


# 4. mongodb管道
class AqiMongodbPipeline(object):
    def open_spider(self, spider):  # 在爬虫开启的时候执行一次
        if spider.name == "aqi":

            self.con = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient

            self.collection = self.con["AQI"]["aqi_data"]  # 创建数据库名为tencent,集合名为tencent_zhaopin的集合操作对象

    def process_item(self, item, spider):
        if spider.name == "aqi":
            self.collection.insert(dict(item))  # item对象先转为字典，再插入
        return item  # 传递给权限低的管道

    def close_spider(self, spider):
        self.con.close()


# 5.redis管道
class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.client = redis.Redis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        self.client.lpush('aqi_list_mo', dict(item))
        return item
