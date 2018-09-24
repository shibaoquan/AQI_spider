# -*- coding: utf-8 -*-
import scrapy
from AQI.items import AqiItem



class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'

    # 1. 请求首页
    start_urls = ['https://www.aqistudy.cn/historydata/']

    # 2. 解析出所有的 城市名字和link
    def parse(self, response):

        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()[16:17]
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()[16:17]

        for city_name, city_link in zip(city_name_list, city_link_list):
            item = AqiItem()
            item['city_name'] = city_name

            # 发送城市的请求url request
            url = self.base_url + city_link
            yield scrapy.Request(url, callback=self.parse_month, meta={'citykey': item})

    # 3. 解析月份的链接
    def parse_month(self, response):

        # 取出从首页传入的item
        item = response.meta['citykey']

        # 解析出月份链接
        month_link_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/a/@href').extract()[2:3]

        # 发送月份的请求 获取每天数据
        for month_link in month_link_list:
            url = self.base_url + month_link
            yield scrapy.Request(url, callback=self.parse_day, meta={'citykey':item})


    # 4. 解析目标数据 每天的数据
    def parse_day(self, response):

        # 取出从首页传入的item
        item = response.meta['citykey']

        tr_list = response.xpath('//tr')

        # 删除表头
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

            yield item
















