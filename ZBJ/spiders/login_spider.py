# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest

from ZBJ.settings import *


class LoginSpiderSpider(CrawlSpider):
    name = 'login_spider'
    allowed_domains = ['zbj.com']
    start_urls = ['http://task.zbj.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93']

    rules = (
        Rule(LinkExtractor(allow=r''),),
    )

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies,
                              callback = self.parse_item)#jump to login page

    def parse_item(self, response):
        content = response.body
        with open('url.html', 'w') as fp:
            fp.write(content)
