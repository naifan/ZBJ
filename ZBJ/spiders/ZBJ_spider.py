# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url 

from ZBJ.items import ZBJItem
#from loginform import fill_login_form
import urllib
import os
import subprocess

class ZBJSpider(Spider):
    name = "ZBJ"
    allowed_domins = ["zhubajie.com"]
    start_urls = ["http://task.zbj.com/success/?kw=百度知道"]

    login_url = 'https://login.zbj.com/login'
    login_user = ''
    login_password = ''

    def start_requests(self):
        self.logger.info('start_requests')
        yield Request(self.login_url, self.parse_login)

    def parse_login(self, response):
        self.logger.info('parse_login')
        with open('login_page.html', 'w') as fp:
            fp.write(response.body)
        img_src_relative = response.xpath('//*[@id="login"]/div/div[3]/a/img/@src').extract()
        print "*******************"
        print img_src_relative
        base_url = get_base_url(response)
        img_src = urljoin_rfc(base_url, img_src_relative)
        print "img_src "  +img_src
        try:
            os.remove("captcha.png")
        except:
            pass
        urllib.urlretrieve(img_src[0], "captcha.png")

        captcha = raw_input("put captcha in mannully>")
        print captcha 

    def start_crawl(self, response):
        self.logger.info('start_crawl')
        if "账号或密码错误" in response.body:
            self.logger.error("Login failed")

        if "退出登录" in response.body:
            self.logger.info('Success login')
        content = response.body
        with open('url.html', 'w') as fp:
            fp.write(content)
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        tasks = Selector(response).xpath('//div[@class="success-task-list clearfix" ]/ul')

        for task in tasks:
            item = ZBJItem()
            item['title'] = task.xpath('li[@class="task-item-title-li"]/a/text()').extract()[0]
            item['url'] = task.xpath('li[@class="task-item-title-li"]/a/@href').extract()[0]
            yield item
            
