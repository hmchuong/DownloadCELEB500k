# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Celeb500KItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    image_dir = scrapy.Field()
