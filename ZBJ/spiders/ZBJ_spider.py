# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from ZBJ.items import ZBJItem
from loginform import fill_login_form

class ZBJSpider(Spider):
    name = "ZBJ"
    allowed_domins = ["zhubajie.com"]
    start_urls = ["http://task.zhubajie.com/success/?kw=百度知道"]

    login_url = 'https://login.zhubajie.com/login'
    login_user = ''
    login_password = ''

    def start_request(self):
        yield Request(self.login_url, self.parse_login)

    def parse_login(self, response):
        data, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_password)
        return FormRequest(url, formdata=dict(data), method=method, callback=start_crawl)

    def start_crawl(self, response):
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        tasks = Selector(response).xpath('//div[@class="success-task-list clearfix" ]/ul')

        for task in tasks:
            item = ZBJItem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()[0]
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()[0]
            yield item
            
