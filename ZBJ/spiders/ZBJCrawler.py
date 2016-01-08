# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url

from ZBJ.items import ZBJItem
#from loginform import fill_login_form
from ZBJ.settings import *


#处理空格
def process_value(v):    
    v1 = v.split()[-1]
    if v1.startswith('http'):
        v = v1
    return v

class ZbjcrawlerSpider(CrawlSpider):
    name = 'ZBJCrawler'
    allowed_domains = ['zbj.com']
    start_urls = ['http://task.zbj.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93']

    #rules = [
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        #提取下一页链接
    #    Rule(LinkExtractor(restrict_xpaths=('//div[@class="pagination"]'), process_value=process_value ), 
    #                       callback='parse_start_url', follow=True),
        #Rule(LinkExtractor(allow=r'task.zhubajie.com/\d+', restrict_xpaths=('//div[@class="pagination"]')),
        #                   callback='parse_10', follow=True),

    #]

    login_url = ['http://u.zbj.com/task/order',]
    # login_user = ''
    # login_password = ''

    # def start_requests(self):
        # self.logger.info('start_requests')
        # yield Request(self.login_url, self.parse_login)

    # def parse_login(self, response):
        # self.logger.info('parse_login')
        # data, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_password)
        # return FormRequest(url, formdata=dict(data), method=method, callback=self.start_crawl)
    def __init__(self, *a, **kwargs):
        super(ZbjcrawlerSpider, self).__init__(*a, **kwargs)   #overdide methods of derived class, in addition to new code. need to call Super method manully
        self.headers = HEADER
        self.cookies = COOKIES
        self.id = 0

    def start_requests(self):
        for i, url in enumerate(self.login_url):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies,
                              callback = self.start_crawl)#jump to login page


    def start_crawl(self, response):
        self._log_page(response, 'ZBJLogin.html')
        self.logger.info('start_crawl')
        # if "authentication failed" in response.body:
            # self.logger.error("Login failed")
        if "Wilna" in response.body:
            self.logger.info("Login success")
        print response.meta['cookiejar']  # 输出0，cookiejar不起作用
        for url in self.start_urls:
            print url
            yield Request(url, \
            headers = self.headers, \
            #meta = {'cookiejar': response.meta['cookiejar'],\
            cookies =self.cookies,\
            #},\
            callback = self.parse_start_url   #替换rule,
            #第一页没有抓取，更改start_urls的调用函数为parse_start_url
            )
    
    def parse_start_url(self, response):
        page_urls = response.xpath('//div[@class="pagination"]/ul/li/a/@href').extract()
        
        for url in page_urls:
            print url
            url = process_value(url)
            print url
            
            yield Request(url,\
                headers = self.headers,\
                #meta = {'cookiejar': response.meta['cookiejar'],\
                cookies =self.cookies, \
                #},\
                callback = self.parse_page_url   #抓取页面链接
                )
		
    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))

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

    def parse_page_url(self, response):
        self.id = self.id + 1
        self._log_page(response, "%d.html" % self.id)
        urls = response.xpath('//div[@class="success-task-list clearfix"]/ul/li[@class="task-item-title-li"]/a/@href').extract()
        for url in urls:
            self.logger.info('Parse_0 '+ url)
            yield Request(url,\
                    headers = self.headers,\
                    #meta = {'cookiejar': response.meta['cookiejar'],\
                    cookies =self.cookies, \
                    #},\
                    #callback=self.parse_10  #
                    callback = self.parse_page
                   )  
            #不用callback？
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
    def parse_page(self, response):
        page_urls = response.xpath('//div[@class="pagination"]/ul/li/a/@href')
        for page_url in page_urls:
            #url_short = page_url.xpath('@href').extract()[0]  #List index out of range: a中不全有/@href，超过10后有'...'
            url_short = page_url.extract()[0]
            print "url_short: " + url_short
            url = urljoin_rfc(get_base_url(response), url_short)
            print "url: " + url
            yield Request(url, \
                headers = self.headers,\
                cookies = self.cookies,\
                callback = self.parse_10,
                )
        #通过循环实现
        # nextLink = response.xpath('//div[@class="pagination"]/ul/li/a/')
        # if nextLink.xpath('text()').extract()[0] == u'\xbb':
            # nextLink = href
            # print nextLink
            # yield Request(callback = parse_page)

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
        #self.id = self.id + 1
        #self._log_page(response, "%d.html" % self.id)
        
        item = ZBJItem()
        item['url'] = response.url
        if ( response.xpath('//h1/text()').extract()):
            item['title'] = response.xpath('//h1/text()').extract()
        else:
            item['title'] = ""
        if (response.xpath('//p[@class="bidc"]/text()').extract()):
            item['content'] = response.xpath('//p[@class="bidc"]/text()').extract()
        else:
            item['content'] = ""
        yield item
        # titles = response.xpath('//h1/text()').extract()
        # urls = response.url
        # contents = response.xpath('//p[@class="bidc"]/text()').re('-\s[^\n]*\\r')

        # for title, url, content in zip(titles, urls, contents):
        #     self.logger.info('Parse_10 '+ response.url)
        #     item = ZBJItem()
        #     item['title'] = title
        #     item['url'] = url
        #     item['content'] = content
        #     yield item

    



