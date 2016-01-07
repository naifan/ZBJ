# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url

from ZBJ.settings import *
from ZBJ.items import ZBJItem

class LoginSpiderSpider(CrawlSpider):
    name = 'login_spider'
    allowed_domains = ['zbj.com']
    #start_urls = ['http://task.zbj.com/success/?kw=%E7%99%BE%E5%BA%A6%E7%9F%A5%E9%81%93']
    #start_urls = ['http://u.zbj.com/task/order']
    start_urls = ['http://task.zbj.com//4750773/']

    rules = (
        Rule(LinkExtractor(allow=r''), ),
    )

    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield FormRequest(url, meta = {'cookiejar': i}, \
                              headers = self.headers, \
                              cookies =self.cookies, \
                              #callback = self.parse_item
                              callback = self.parse_page,\
                              )#jump to login page

    def parse_item(self, response):
        content = response.body
        with open('url.html', 'w') as fp:
            fp.write(content)
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
    
    def parse_page(self, response):
        page_urls = response.xpath('//div[@class="pagination"]/ul/li/a')
        for page_url in page_urls:
            url_short = page_url.xpath('@href').extract()[0]
            print "url_short: " + url_short
            url = urljoin_rfc(get_base_url(response), url_short)
            print "url: " + url
            yield Request(url, \
                headers = self.headers,\
                cookies = self.cookies,\
                callback = self.parse_item,
                )
        
               
                    
                
    
                