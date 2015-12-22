# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest

from ZBJ.items import ZBJItem
from loginform import fill_login_form


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
        Rule(LinkExtractor(allow=r'task.zhubajie.com/success/', restrict_xpaths=('//div[@class="pagination"]'),
                           process_value=process_value), callback='parse_start_url', follow=True),
        Rule(LinkExtractor(allow=r'task.zhubajie.com/\d+', restrict_xpaths=('//div[@class="pagination"]')),
                           callback='parse_10', follow=True),

    ]

    def parse_item(self, response):
        i = ZBJItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

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
        urls = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
        for url in urls:
            self.logger.info('Parse_0 '+ response.url)
            yield Request(url)  #不用callback？
        # titles = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/text()').extract()
        # urls = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
        # contents = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
    
        # for title, url, content in zip(titles, urls, contents):
        #     self.logger.info('parse_0 '+ response.url)
        #     item = ZBJItem()
        #     item['title'] = title
        #     item['url'] = url
        #     #未登录
        #     #request = Request(content, callback = self.parse_1)
        #     #登录
        #     request = Request(content, callback = self.parse_10）
        #     request.meta['item'] = item
        #     yield request


    #未登录抓取目标页面
    def parse_1(self, response):
        self.logger.info('Parse_1 '+ response.url)
        item = response.meta['item']
        if (response.xpath('//p[@class="detail-anthor"]/text()').extract()):
            item['content'] = response.xpath('//p[@class="detail-anthor"]/text()').extract()
        else:
            item['content'] = ""
        yield item

    #登录抓取
    def parse_10(self, response):
        self.logger.info('Parse_10 '+ response.url)
        titles = response.xpath('//h1/text()').extract()
        urls = response.url
        contents = response.xpath('//p[@class="bidc"]/text()').re('-\s[^\n]*\\r')

        for title, url, content in zip(titles, urls, contents):
            self.logger.info('Parse_10 '+ response.url)
            item = ZBJItem()
            item['title'] = title
            item['url'] = url
            item['content'] = content
            yield item

    



