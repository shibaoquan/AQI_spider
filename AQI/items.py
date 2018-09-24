# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):

    # 城市名字
    city_name = scrapy.Field()

    # 日期
    date = scrapy.Field()
    # AQI
    aqi = scrapy.Field()
    # 质量等级
    level = scrapy.Field()
    # PM2.5
    pm2_5 = scrapy.Field()
    # PM10
    pm10 = scrapy.Field()
    # 二氧化硫
    so_2 = scrapy.Field()
    # 一氧化碳
    co = scrapy.Field()
    # 二氧化氮
    no_2 = scrapy.Field()
    # 臭氧
    o3 = scrapy.Field()

    # 数据源的字段
    data_time = scrapy.Field()
    spider = scrapy.Field()


