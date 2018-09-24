# -*- coding: utf-8 -*-

# Scrapy settings for AQI project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'AQI'

SPIDER_MODULES = ['AQI.spiders']
NEWSPIDER_MODULE = 'AQI.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'AQI (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'AQI.middlewares.ChromeMidddlewares': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'AQI.middlewares.ChromeMidddlewares': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'AQI.pipelines.AqiDataPipeline': 200,
    'AQI.pipelines.AqiJsonPipeline': 300,
    'AQI.pipelines.AqiCsvPipeline': 400,
    # "AQI.pipelines.AqiMongodbPipeline": 500,
    # "AQI.pipelines.AqiRedisPipeline": 600
    # 分布式 自带的管道存储数据
    'scrapy_redis.pipelines.RedisPipeline': 400


}


# 1.设置 分布式的 去重组件
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 2.设置 分布式的 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 3.允许爬虫中途停止 中断
SCHEDULER_PERSIST = True

# 4.设置 redis 数据库的端口号 和IP
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379