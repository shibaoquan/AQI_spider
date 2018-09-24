# -*- coding: utf-8 -*-
import scrapy
from AQI.items import AqiItem
from scrapy.spiders import  Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class AqiSpider(RedisCrawlSpider):
    name = 'aqi_crawl_redis'
    # 改域名
    allowed_domains = ['aqistudy.cn']

    redis_key = 'aqicrawlredis'

    # callback 有; follow False
    # callback 没有 follow True

    rules = (
        # 自动提取 所有城市的链接,自动发送请求 解析link
        Rule(LinkExtractor(allow='monthdata\.php')),

        # 自动提取 所有月份的链接,自动发送请求 解析link, 手动解析data
        Rule(LinkExtractor(allow="daydata\.php"), callback="parse_day", follow=False),
    )

    # 4.解析目标数据 每天的数据
    def parse_day(self, response):

        item = AqiItem()

        # 解析 标题 在提取城市名字
        title = response.xpath('//*[@id="title"]/text()').extract_first()
        item['city_name'] = title[8:-11]

        # 1. 取出所有 tr_list
        tr_list = response.xpath('//tr')

        # 2.删除表头
        tr_list.pop(0)

        for tr in tr_list:
            # 日期
            item['date'] = tr.xpath('./td[1]/text()').extract_first()
            # AQI
            item['aqi'] = tr.xpath('./td[2]/text()').extract_first()
            # 质量等级
            item['level'] = tr.xpath('./td[3]//text()').extract_first()
            # PM2.5
            item['pm2_5'] = tr.xpath('./td[4]/text()').extract_first()
            # PM10
            item['pm10'] = tr.xpath('./td[5]/text()').extract_first()
            # 二氧化硫
            item['so_2'] = tr.xpath('./td[6]/text()').extract_first()
            # 一氧化碳
            item['co'] = tr.xpath('./td[7]/text()').extract_first()
            # 二氧化氮
            item['no_2'] = tr.xpath('./td[8]/text()').extract_first()
            # 臭氧
            item['o3'] = tr.xpath('./td[9]/text()').extract_first()

            # 将数据 -->engine-->pipeline
            yield item
