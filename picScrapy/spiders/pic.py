# -*- coding:utf-8 -*-
# ! /bin/bash/python3

import re
from urllib.parse import urljoin
from scrapy.spiders import Spider
from scrapy.http import Request
from picScrapy.items import PicscrapyItem


class PicSpider(Spider):
    name = "pic"  # 定义爬虫名
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    }

    def start_requests(self):
        for i in range(1, 31):
            url = 'http://www.jj20.com/bz/nxxz/list_7_cc_14_%d.html' % i
            yield Request(url, headers=self.headers)

    # 一级页面的处理函数
    def parse(self, response):
        # 提取界面所有的符合入口条件的url
        all_urls = response.xpath('//div[@class="main"]/ul/li/a[1]/@href').extract()
        # 遍历获得的url，继续爬取
        for url in all_urls:
            # urljoin生成完整url地址
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_img)

    # 二级页面的处理函数
    def parse_img(self, response):
        item = PicscrapyItem()
        # 提前页面符合条件的图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        title = response.xpath('/html/body/div[3]/h1/span/text()').extract()[0]
        item['title'] = title.split('(')[0] + '(' + re.search(r'(\d+)/(\d+)', title).group(2) + ')'
        yield item
        # 提取界面所有复合条件的url
        all_urls = response.xpath('//ul[@id="showImg"]/li/a/@href').extract()
        # 遍历获得的url，继续爬取
        for url in all_urls:
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_img)
