#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
import codecs
from bingproxy import BingProxy

class MusicSpider(scrapy.Spider):
    name = "Music"
#    allowed_domains = ["tyst.migu.cn"]
    start_urls = []  
    bingProxy = BingProxy()

    def start_requests(self):
        with open('todo_url.txt') as url_list:
            for url in url_list:
                url = url.strip()
                #yield scrapy.Request(url = self.bingProxy.get_proxy_url(url), meta = {"origin_rul": url}, callback = self.parse )
                yield scrapy.Request(url = url,meta = {"origin_url": url}, callback=self.parse)
    #def __init__(self, urlfile=None,*args, **kwargs):
     #   super(MusicSpider, self).__init__(*args, **kwargs)
      #  uf = codecs.open(urlfile, 'r', 'utf-8')
       # urls = [line.strip() for line in uf.readlines()]
        #self.start_urls = urls

    
    def parse(self, response):
        path = response.url.split('/')[-1]
        path = path.split('?')[0]
        self.logger.info('Saving mp3 %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)


