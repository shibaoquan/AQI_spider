# -*- coding: utf-8 -*-
import scrapy
from AQI.items import AqiItem
from scrapy_redis.spiders import RedisSpider

class AqiSpider(RedisSpider):
    name = 'aqi_redis'
    # 改域名
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'

    redis_key = 'aqiredis'

    # 2.解析出所有的 城市名字和link
    def parse(self, response):
        # 城市名字和link
        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()[
                         10:11]
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()[
                         10:11]

        for city_name, city_link in zip(city_name_list, city_link_list):
            item = AqiItem()
            item['city_name'] = city_name

            # 发送城市的请求url request
            url = self.base_url + city_link
            yield scrapy.Request(url, meta={'citykey': item}, callback=self.parse_month)

    # 3.解析月份的链接
    def parse_month(self, response):
        # 取出从首页传入的item
        item = response.meta['citykey']

        month_link_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/a/@href').extract()[5:6]

        # 发送月份的请求 获取每天的数据
        for month_link in month_link_list:
            url = self.base_url + month_link
            yield scrapy.Request(url, meta={'citykey': item}, callback=self.parse_day)

    # 4.解析目标数据 每天的数据
    def parse_day(self, response):

        # 取出传入的城市 item
        item = response.meta['citykey']

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
