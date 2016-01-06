# -*- coding: utf-8 -*-

# Scrapy settings for ZBJ project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ZBJ'

SPIDER_MODULES = ['ZBJ.spiders']
NEWSPIDER_MODULE = 'ZBJ.spiders'

ITEM_PIPELINES = {
    #'ZBJ.pipelines.MongoDBPipeline',
    'ZBJ.pipelines.JsonWithEncodingPipeline': 1,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "ZBJ"
MONGODB_COLLECTION = "zbjbaidu"

DOWNLOAD_DELAY = 5
#LOG_LEVEL = 'INFO'
HEADER = {
    "Host": "task.zbj.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
    }

# COOKIES = {
    #'uniqid': r'93168344e1d25c42d19ea53158f39feb',  #过期时间，浏览会话结束时
    # '_uq': r'75888216c3f0ce8edf087e3f91ab342e',
    # 'defaultShowService': r'1',
    # 'userkey': r'm7frgZbJCQdj8%2BgYREGoA6q0Of9bMnqZ3HKLF8Mm33YwuuHKCKiBq%2F6uGeWZUmj%2BGOgwrGHCUaS4wwxgbonqzLld4jellKBD2ps3d%2BO9BxODfjvQyjn7U8AyoOt6m2qB5oKDg2NAujOdUFZ%2BhUkltjQviCjur9RYYzxcygOiaPUNoh4mnXxpshYYCZxFs%2Bb1yzpUZAbxsmhK0sndLszizyMHVdBaMmoErFeo7guX7SuD%2F8f8RlplojHQZ65%2Frvsg',
    # 'userid': r'12489963',
    # 'nickname': r'Wilna',
    # 'brandname': r'Wilna',
    # '_uv': r'11',
    # 'viewed_task': r'12489963%3A6739168%2C6736033%2C6734875',
    # '_ga': r'GA1.2.281368141.1451351506',
    # 'Hm_lvt_a9be76f51f7880c755391d2e0ff3e4f8': r'1451351505',
    #'Hm_lpvt_a9be76f51f7880c755391d2e0ff3e4f8': r'1451391421',
    # '__utma': r'168466538.281368141.1451351506.1451384045.1451391421.6',
    # '__utmb': r'168466538.1.10.1451391421',
    #'__utmc': r'168466538',
    # '__utmz': r'168466538.1451375989.4.2.utmcsr=zbj.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga=GA1.3.281368141.1451351506',
    #'footerBarStateTask': r'0',
    # }
COOKIES = {
    '__utma': r'168466538.1963172230.1451904720.1451972889.1452001329.8',  #1
	'__utmb': r'168466538.1.10.1452001329',   #2
	'__utmz': r'168466538.1451904720.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
	'_uq': r'd41d8cd98f00b204e9800998ecf8427e',
	'_ga': r'GA1.3.1963172230.1451904720', #4
	'_gat': r'1',
	'__utmt': r'1',
    '_ga': 'GA1.2.1963172230.1451904720', #two
	'userkey': r'g9tptvxJk3be1qHB4NfJqqB5aB56INWLTaQKxAJIxaikzpfC64ynfd5zKe0vVPn1STkJ8cv1Zk81Qo4RKVk7EDGyyiTLXEHlI4YcgF0W11r1YFCBT18rew4tv2FfbzAsUqb%2FY4ZGKXTF0gfGaSA7w9%2BX%2BSPJerg4Skye88JP5oe0mpjZuHMubFa2h8oEx%2Fjx95K8mUn1uE4hWTauJ5ofRRFHLr4pcCQhn794%2BmWdchdjAvTlx8wmH7p%2B1EtT8PSdpmo%3D',
	'userid': r'12489963',
	'nickname': r'Wilna',
	'brandname': r'Wilna',
	'uniqid': r'add0f0994e4ce44c606011bec42e256b', #3
	'__utmc': r'168466538',
	#'webimMainPage': r'6r8u1vbzvpnn', 
    #new
    #'PHPSESSID': r'gd7369ufss4g5nrgcshatj9cf0',
    #'defaultShow': r'2',
    #'taskid': r'6746770',
    '_analysis': r'a53bOOaaa0k%2FfyjvoqGY1o2hyAVLvKlUeb%2BAK0EmPwvjJnJzopfiqzU3KwQRno%2BXImfJPC1eg7bkpMwTj6F%2F3V5a2nR0qEBp',
    'fvtime': r'8956fNKzGD7SQRclIibcvc8nXnLIUsW3zeJLtgW8brnBw6LaV8lz', 
	}
 #   PHPSESSID=gd7369ufss4g5nrgcshatj9cf0; defaultShow=2; taskid=6746770; _analysis=a53bOOaaa0k%2FfyjvoqGY1o2hyAVLvKlUeb%2BAK0EmPwvjJnJzopfiqzU3KwQRno%2BXImfJPC1eg7bkpMwTj6F%2F3V5a2nR0qEBp; fvtime=8956fNKzGD7SQRclIibcvc8nXnLIUsW3zeJLtgW8brnBw6LaV8lz; 
 # _ga=GA1.3.1963172230.1451904720; __utma=168466538.1963172230.1451904720.1451972889.1452001329.8;
 #  _ga=GA1.2.1963172230.1451904720;   fvtime=8956fNKzGD7SQRclIibcvc8nXnLIUsW3zeJLtgW8brnBw6LaV8lz
