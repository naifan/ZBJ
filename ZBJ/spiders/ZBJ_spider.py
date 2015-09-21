# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector

from ZBJ.items import ZBJItem

class ZBJSpider(Spider):
    name = "ZBJ"
    allowed_domins = ["zhubajie.com"]
    start_urls = ["http://task.zhubajie.com/success/?kw=百度知道"]

    def parse(self, response):
        tasks = Selector(response).xpath('//div[@class="success-task-list clearfix" ]/ul')

        for task in tasks:
            item = ZBJItem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()[0]
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()[0]
            yield item
            
