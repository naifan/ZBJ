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
    name = 'ZBJCrawler2'
    allowed_domains = ['zbj.com']
    #start_urls = ['http://task.zbj.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93']
    start_urls = ['http://search.zbj.com/t/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93&type=']

    #login_url = ['http://task.zbj.com/4750773/',]
    login_url = ['http://u.zbj.com/task/order',]
 
    def __init__(self, *a, **kwargs):
        super(ZbjcrawlerSpider, self).__init__(*a, **kwargs)   #overdide methods of derived class, in addition to new code. need to call Super method manully
        self.headers = HEADER
        self.cookies = COOKIES
        self.id = 0

    def start_requests(self):
        for i, url in enumerate(self.login_url):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies = self.cookies,
                              callback = self.start_crawl)#jump to login page


    def start_crawl(self, response):
        self._log_page(response, 'ZBJLogin.html')
        self.logger.info('start_crawl')
        if "Wilna" in response.body:
            self.logger.info("Login success")
        #print response.meta['cookiejar']  # 输出0，cookiejar不起作用
        for url in self.start_urls:
            print url
            yield Request(url, \
            headers = self.headers, \
            # meta = {'cookiejar': response.meta['cookiejar'],\
            cookies =self.cookies,\
            #},\
            callback = self.parse_start_url   #替换rule,
            #第一页没有抓取，更改start_urls的调用函数为parse_start_url
            )
    
    def parse_start_url(self, response):
        self.logger.info('Parse_1 '+ response.url)
        tasks = response.xpath('//a[@class = "list-task-title"]/@href').extract()
        for task in tasks:
            #self.logger.info('Parse_0 '+ task)
            yield Request(task,\
                    headers = self.headers,\
                    #meta = {'cookiejar': response.meta['cookiejar'],\
                    cookies =self.cookies, \
                    #},\
                    callback = self.parse_page
                   )          
        nextLink = response.xpath('//div[@class="pagination"]/ul/li/a')
        print nextLink.xpath('text()').extract()
        if nextLink.xpath('text()').extract()[-1] == u'\xbb':
            nextLink = nextLink.xpath('@href').extract()[-1]
            print "nextLink 1: " + nextLink
            # print "base_url: " + get_base_url(response)
            # nextLink = urljoin_rfc(get_base_url(response), nextLink)
            # print "nextLink 2: " + nextLink
            yield Request(nextLink, \
                headers = self.headers,\
                cookies = self.cookies,\
                # meta = {'cookiejar': response.meta['cookiejar'],}, \
                callback = self.parse_start_url,
                )    
		
    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))

    def parse_page(self, response):
        self.logger.info('Parse_2 '+ response.url)
        item = ZBJItem()
        item['url'] = response.url
        if ( response.xpath('//h1/text()').extract()):
            item['title'] = map(unicode.strip, response.xpath('//h1/text()').extract())
        else:
            item['title'] = ""
        if (response.xpath('//p[@class="bidc"]/text()').extract()):
            item['content'] = map(unicode.strip, response.xpath('//p[@class="bidc"]/text()').extract())
        else:
            item['content'] = ""
        yield item
      
        #下一页 
        if (response.xpath('//div[@class="pagination"]/ul/li/a')):
            nextLink = response.xpath('//div[@class="pagination"]/ul/li/a')
            print nextLink.xpath('text()').extract()
            if nextLink.xpath('text()').extract()[-1] == u'\xbb':
                nextLink = nextLink.xpath('@href').extract()[-1]
                print "nextLink 1: " + nextLink
                print "base_url: " + get_base_url(response)
                nextLink = urljoin_rfc(get_base_url(response), nextLink)
                print "nextLink 2: " + nextLink
                yield Request(nextLink, \
                    headers = self.headers,\
                    cookies = self.cookies,\
                    # meta = {'cookiejar': response.meta['cookiejar'],}, \
                    callback = self.parse_page,
                    ) 

    



