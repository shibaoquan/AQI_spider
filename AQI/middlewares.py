# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import scrapy
import time


# 自定义下载器Chrome()
class ChromeMidddlewares(object):
    def process_request(self, request, spider):
        url = request.url
        if url != 'https://www.aqistudy.cn/historydata/':
            # 1. 创建 无头浏览器对象
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)

            # driver = webdriver.Chrome()  # 有头浏览器

            # 发送请求
            driver.get(url)

            # 注意添加延迟
            time.sleep(3)

            # 获取数据
            data = driver.page_source

            # 关闭数据
            driver.quit()

            # 将自定义的下载器包装成response对象： HttpResponse
            return scrapy.http.HtmlResponse(url=url, body=data.encode('utf-8'), encoding='utf-8', request=request)
