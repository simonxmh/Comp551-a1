# -*- coding: utf-8 -*-
import scrapy


class ChoualboxSpider(scrapy.Spider):
    name = 'choualbox'
    allowed_domains = ['choualbox.com']
    start_urls = ['http://choualbox.com/']

    def parse(self, response):
        pass
