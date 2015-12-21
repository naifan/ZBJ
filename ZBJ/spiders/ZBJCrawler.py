# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from ZBJ.items import ZBJItem


#处理空格
def process_value(v):    
    v1 = v.split()[-1]
    if v1.startswith('http'):
        v = v1
    return v

class ZbjcrawlerSpider(CrawlSpider):
    name = 'ZBJCrawler'
    allowed_domains = ['zhubajie.com']
    start_urls = ['http://task.zhubajie.com/success/?kw=百度知道']

    rules = [
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        #提取下一页链接
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="pagination"]'),
                           process_value=process_value), callback='parse_start_url', follow=True),

    ]

    def parse_item(self, response):
        i = ZBJItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    #抓取成功的campaign
    def parse_0(self, response):
        tasks = response.xpath('//div[@class="success-task-list clearfix"]/ul')
        for task in tasks:
            self.logger.info('parse_0', response.url)
            item = ZBJItem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()
            print item
            yield item

    def parse_start_url(self, response):
        # urls = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
        # for url in urls:
        #     return scrapy.Request(url, callback=self.parse_1)
        titles = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/text()').extract()
        urls = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
        contents = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
    
        for title, url, content in zip(titles, urls, contents):
            self.logger.info('parse_0 '+ response.url)
            item = ZBJItem()
            item['title'] = title
            item['url'] = url
            request = Request(content, callback = self.parse_1)
            request.meta['item'] = item
            yield request

        
    def parse_1(self, response):
        self.logger.info('Parse_1 '+ response.url)
        item = response.meta['item']
        if (response.xpath('//p[@class="detail-anthor"]/text()').extract()):
            item['content'] = response.xpath('//p[@class="detail-anthor"]/text()').extract()
        else:
            item['content'] = ""
        yield item

    



