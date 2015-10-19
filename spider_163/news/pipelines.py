# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import codecs
import time
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class NewsPipeline(object):
	def __init__(self,dbpool):
		self.dbpool = dbpool
	@classmethod
	def from_settings(cls,settings):
		dbargs = dict(
			host = settings["MYSQL_HOST"],
			db = settings["MYSQL_DBNAME"],
			user=settings['MYSQL_USER'],
			passwd=settings['MYSQL_PASSWD'],
			charset='utf8',
			cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode= True,
			)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	#pipeline默认调用
	def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_upinsert,item,spider)
		d.addErrback(self._handle_error,item,spider)
		d.addBoth(lambda _:item)
		return d

	#将每行跟新写入数据库中
	def _do_upinsert(self,conn,item,spider):
		types = ["news","money","tech","war","ent","mobile","travel","lady","play","auto","edu","baby","digi"]
		newstype = {"news":"新闻","money":"财经","tech":"科技","war":"军事","ent":"娱乐","mobile":"手机","travel":"旅行","lady":"女人",
		"play":"游戏","auto":"汽车","edu":"教育","baby":"亲子","digi":"数码"}
		linkmd5id = self._get_linkmd5id(item)
		length = len(item["picurl"])
		newsTime = datetime.utcnow().replace(microsecond=0).isoformat(' ')
		picture_id = self._get_pictureid(item)
		newsLable = self._get_newsLable(item)
		conn.execute("""
		select 1 from app_news where urlmd5id = %s
		""",(linkmd5id,))
		ret = conn.fetchone()
		if ret:
			pass
		else:
			for indx in types:
				if indx in item["url163"]:
					conn.execute("""
					insert into app_news(urlmd5id,picture_id,newsTitle, newsUrl ,newsLable, newsContent,newsType,newsAbstract
					,newsTime,browseNumber,commentNumber,likesNumber) 
					values(%s,%s,%s,%s,%s,%s,%s,%s,%s,0,0,0)
			    		""", (linkmd5id,picture_id, item['title'],item['url163'],newsLable,item["content"],newstype[indx],item["newsabstract"],newsTime)
			    		)
					print "888888888888888888888888"
				else:
					pass
			if length == 0:
				pass
			else:
				for i in range(length):
					conn.execute('''
			    		insert into app_picture(picture,pictureID)
			    		values(%s,%s)''',(item["picurl"][i],picture_id))
					print "99999999999999999999999999"



	def _get_linkmd5id(self,item):
		return md5(item["url163"]).hexdigest()

	def _handle_error(self,failure,item,spder):
		log.err(failure)

	def _get_pictureid(self,item):
		return str(int(1000 * time.time()))


	def _get_newsLable(self,item):
		return "xxxxx"