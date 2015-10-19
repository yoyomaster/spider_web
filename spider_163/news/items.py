# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	linkmd5id = scrapy.Field()
	title = scrapy.Field()
	url163 = scrapy.Field()
	content = scrapy.Field()
	newsabstract = scrapy.Field()
	picurl = scrapy.Field()