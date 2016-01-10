# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Rule
from scrapy.http import Request, FormRequest
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url

from ZBJ.settings import *
from ZBJ.items import ZBJItem

class LoginSpiderSpider(Spider):
    name = 'login_spider'
    allowed_domains = ['zbj.com']
    #start_urls = ['http://task.zbj.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93']
    start_urls = ['http://u.zbj.com/task/order']
    # start_urls = ['http://task.zbj.com/4750773/']

    # rules = (
        # Rule(LinkExtractor(allow=r''), ),
    # )

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies, \
                              # callback = self.parse_item
                              callback = self.parse_page \
                              )#jump to login page

    def parse_item(self, response):
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
        print response.meta['cookiejar']
        #下一页 
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
                #cookies = self.cookies,\
                meta = {'cookiejar': response.meta['cookiejar'],}, \
                callback = self.parse_item,
                )    
               
    def _log_page(self, response, filename):
        with open(filename, 'w') as f:
            f.write("%s\n%s\n%s\n" % (response.url, response.headers, response.body))      
    
    def parse_page(self, response):
        self._log_page(response, 'login.html')

 
               
                    
                
    
                