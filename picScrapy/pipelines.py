# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
import hashlib
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.utils.python import to_bytes


class PicscrapyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            if re.match(r'http', url):
                yield Request(url)

    def file_path(self, request, response=None, info=None):
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return '%s.jpg' % image_guid
