# -*- coding:utf-8 -*-
# ! /bin/bash/python3

import re
from urllib.parse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request
from picScrapy.items import PicscrapyItem


class PicSpider(Spider):
    name = "pic"  # 定义爬虫名
    start_url = 'http://www.jj20.com'  # 爬虫入口
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    }

    def start_requests(self):
        for i in range(1, 31):
            url = 'http://www.jj20.com/bz/nxxz/list_7_cc_14_%d.html' % i
            yield Request(url, headers=self.headers)

    # 该函数名不能改变，因为Scrapy源码中默认callback函数的函数名就是parse
    def parse(self, response):
        item = PicscrapyItem()
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        yield item
        # 提取界面所有的url
        all_urls = response.xpath('//a/@href').extract()
        # 遍历获得的url，如果满足条件，继续爬取
        for url in all_urls:
            if re.search(r'\d{4}.html||\d{4}_\d+.html', url):
                url = urljoin(response.url, url)
                yield Request(url, callback=self.parse)
