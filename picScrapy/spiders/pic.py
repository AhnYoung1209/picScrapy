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

        domain = 'http://www.jj20.com/bz/'

        # 定义各个分类的入口
        start_urls = [
            'zrfg/list_1',
            'dwxz/list_2',
            'hhzw/list_3',
            'jzfg/list_4',
            'qcjt/list_5',
            'ysbz/list_6',
            'nxxz/list_7',
            'rwtx/list_8',
            'jwxz/list_9',
            'mwjy/list_10',
            'czxt/list_11',
            'sjsh/list_12',
            'ysyx/list_13',
            'tyyd/list_14',
            'ppgg/list_15',
            'ktmh/list_16',
            'shsj/list_17',
            'slkt/list_18',
            'xmsc/list_19',
            'jqqd/list_20',
            'jxbz/list_120',

        ]

        for i in start_urls:
            url = domain + i + '_1.html'
            yield Request(url, headers=self.headers)

    # 一级页面的处理函数
    def parse(self, response):
        # 提取界面所有的符合入口条件的url
        all_urls = response.xpath('//div[@class="main"]/ul/li/a[1]/@href').extract()
        category_name = response.xpath('//li[@class="navnm1"]/a/text()').extract()[0]

        if len(all_urls):
            # 遍历获得的url，继续爬取
            for url in all_urls:
                # urljoin生成完整url地址
                url = urljoin(response.url, url)
                yield Request(url, callback=self.parse_img, meta={'cat': category_name})

            next_url = re.search(r'list_\d+_(\d+)', response.url)
            next_page = str(int(next_url.group(1)) + 1) + '.html'
            # 下一页的url
            next_url = re.sub(r'(\d+).html', next_page, response.url)
            yield Request(next_url, callback=self.parse, meta={'cat': category_name})

    # 二级页面的处理函数
    def parse_img(self, response):
        item = PicscrapyItem()
        # 提取页面符合条件的图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        title = response.xpath('/html/body/div[3]/h1/span/text()').extract()[0]
        item['title'] = title.split('(')[0] + '(' + re.search(r'(\d+)/(\d+)', title).group(2) + ')'
        item['category_name'] = response.meta['cat']
        yield item

        # 提取符合条件的url
        all_urls = response.xpath('//ul[@id="showImg"]/li/a/@href').extract()
        # 遍历获得的url，继续爬取
        for url in all_urls:
            url = urljoin(response.url, url)
            yield Request(url, callback=self.parse_img_img, meta={'cat': response.meta['cat']})

    @staticmethod
    # 三级页面的处理函数
    def parse_img_img(response):
        item = PicscrapyItem()
        # 提取符合条件的图片地址
        item['image_urls'] = response.xpath('//img[@id="bigImg"]/@src').extract()
        title = response.xpath('/html/body/div[3]/h1/span/text()').extract()[0]
        item['title'] = title.split('(')[0] + '(' + re.search(r'(\d+)/(\d+)', title).group(2) + ')'
        item['category_name'] = response.meta['cat']
        yield item
