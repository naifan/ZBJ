# -*- coding: utf-8 -*-
import scrapy
import re
import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ZBJ.items import ZBJItem

class ZbjCrawlerSpider(CrawlSpider):
    name = 'ZBJ_crawler'
    allowed_domains = ['zhubajie.com']
    start_urls = [
        'http://task.zhubajie.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93',
        #'http://task.zhubajie.com/success/p2.html?kw=百度知道',
        #'http://task.zhubajie.com/success/p3.html?kw=百度知道',
        #'http://task.zhubajie.com/success/p4.html?kw=百度知道',
        #'http://task.zhubajie.com/success/p5.html?kw=百度知道',
        #'http://task.zhubajie.com/success/p6.html?kw=百度知道',
    ]

    rules = [
        Rule(LinkExtractor(allow=(r'/success/p[0-9]\.html'),), callback='parse_0', follow=True),
        # Rule(LinkExtractor(restrict_xpaths=('//div[@class="pagination"]'),
        #                   # process_value='process_value'
        # ),
        #      callback='parse_item', follow=True)
        #Rule(LinkExtractor(restrict_xpaths=('//div[@class=success-task-list clearfix]/ul/')),),  #找到任务/numbers返回任务地址

        #Rule(LinkExtractor(restrict_xpaths=('//*[@id="j-works-list"]/dl/dd/div/a[@class="bidid"]')),callback
        #    ='parse+1', follow=True ),   #从/number通过参与编号到达一个提交/num/num或多个
        #Rule(LinkExtractor(restrcit_xpaths=('//a[@class="_target-url"]')),callable='parse_1', follow=True),  #提取更多提交

        #Rule(LinkExtractor(allow=(r'/success/p[0-9]\.html'),), callback='parse_item', follow=True),
        #http://task.zhubajie.com/success/p1.html?kw=百度知道
        #success/p[0-7]\.html
    ]

    # headers = {
    #     "Accept": "application/json, text/javascript, */*; q=0.01",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    #     "Connection": "keep-alive",
    #     "Content-Length": "87",
    #     "Content-Type": "application/x-www-form-urlencoded",
    #     "Referer": "https://login.zhubajie.com/login",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36" ,
    # }
        
    #    #重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    # def start_requests(self):
    #     return [Request("https://login.zhubajie.com/login", meta = {'cookiejar' : 1}, callback = self.post_login)]  #添加了meta

    # #FormRequeset出问题了
    # def post_login(self, response):
    #     print 'Preparing login'
    #     #下面这句话用于抓取请求网页后返回网页中的seed字段的文字, 用于成功提交表单
    #     seed = response.xpath('//input[@name="seed"]/@value').extract()[0]
    #     print seed
    #     #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
    #     #登陆成功后, 会调用after_login回调函数
    #     return [FormRequest.from_response(response,
    #                         meta = {'cookiejar' : response.meta['cookiejar']}, #注意这里cookie的获取
    #                         headers = self.headers,
    #                         formdata = {
    #                             'usename': 'haokqgood@163.com',
    #                             'passwprd': 'shehuozhongde',
    #                             #'catcha': , 
    #                             'seed': seed,
    #                             'fromurl': 'http://task.zhubajie.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93',
    #                         },
    #                         callback = self.after_login,
    #                         dont_filter = True
    #                         )]

    # def after_login(self, response) :
    #     for url in self.start_urls :
    #         yield self.make_requests_from_url(url)
    def parse_0(self, response):
        tasks = response.xpath('//div[@class="success-task-list clearfix"]/ul')
        for task in tasks:
            self.logger.info('parse_0', response.url)
            item = ZBJitem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()
            print item
            yield item 

    def parse_1(self, response):
        tasks = response.xpath('//p[@class="bidc"]')

        for task in tasks:
            self.logger.info('parse_1'+ response.url)
            item = ZBJItem()
            item['url'] = response.xpath('/a[@class="url"]').extract()
            item['title'] = response.xpath('a/text()').extract()
        

    def parse_item(self, response):
        #inspect one response
        if  response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)
            
        tasks = response.xpath('//div[@class="success-task-list clearfix" ]/ul')

        for task in tasks:
            self.logger.info('parse '+response.url)
            item = ZBJItem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()[0]
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()[0]
            print item
            yield item


        

    def process_value(v):
        v1 = v.split()[-1]
        if v1.startwith('http'):
            v = v1
        return v
