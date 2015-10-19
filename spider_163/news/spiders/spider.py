# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor as le
from scrapy.utils.response import get_base_url
from news.items import *

class news_spider(CrawlSpider):
	name = "news_spider"
	allowed_domains = ["163.com"]
	start_urls = ["http://www.163.com",]
	rules = [
        		# Rule(le(allow=(r"news\.\d+\.com/15/\d+/\d+/*")), 
        		Rule(le(allow=(r'/\w+\.163\.com/15/10\d{2}/\d+/\w+\.html')), 
			 follow=True, 
			 callback='parse_item')
        		]
	_x_query = {
    		"title":"""//div[contains(@class, 'ep-content-main')]/h1[contains(@id, "h1title")]/text()""",
    		# "articleurl":'''//div[contains(@class, "ep-time-source cDGray")]/a[contains(@id, "ne_article_source")]/@href''',
    		"content":'''//div[contains(@class, "end-text")]/p/text()''',
    		'picurl':'''//div[contains(@class, "end-text")]/p[contains(@class, "f_center")]/img/@src''',
    		}

    	#定义回调函数
    	#提取数据到Items里面，主要用到XPath和CSS选择器提取网页数据
    	def  parse_item(self,response):
    		items=[]
    		sel = Selector(response)
    		base_url = get_base_url(response)
    		item = NewsItem()
    		item["title"] = response.xpath(self._x_query["title"]).extract()[0]
    		print item["title"]+"*******************\r\n"
    		item["content"] = ""
		con= response.xpath(self._x_query['content']).extract()
		for index in range(len(con)):
		            	item["content"] = item["content"]+con[index]+'\n'
		item["picurl"] = response.xpath(self._x_query["picurl"]).extract()

		item['url163'] = base_url
		item["newsabstract"] = item["content"][:100]+"..."
	       
		items.append(item)
	        	# print items
		return items

