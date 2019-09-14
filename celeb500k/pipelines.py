# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import os
import uuid
import sys

class Celeb500KPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        sys.exit(0)
        request = scrapy.Request(item['image_urls'])
        os.makedirs(item['image_dir'], exist_ok=True)
        request.meta['output'] = os.path.join(item['image_dir'], str(uuid.uuid4())+".jpg")
        yield request
            
    def file_path(self, request, response, info):
        return request['output']
    
    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem("Item contains no images")
    #     item['image_paths'] = image_paths
    #     return item