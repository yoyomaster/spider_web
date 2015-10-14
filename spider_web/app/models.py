#encoding: utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserProfile(models.Model):    #用户信息表 
	user = models.OneToOneField(User)  #与django自带的User表 OneToOne映射
	userGrade = models.IntegerField(default = 1)  #用户等级
	#用户头像
	userImage = models.ImageField(upload_to = 'static/user_image',default='static/images/default.gif', blank = True,null = True)
	loginCount = models.IntegerField(default = 1)  #登陆次数
	lastLogin = models.DateTimeField(auto_now = True)  #最后一次登陆时间
	likeCount = models.IntegerField(default = 0)   #点赞次数
	commentCount = models.IntegerField(default = 0)    #评论次数

	def __unicode__(self):
		return self.user.username


class Picture(models.Model):  #保存新闻中的图片URL
#	picture = models.ImageField(upload_to = 'news_images', blank = True)
	picture = models.URLField(max_length = 256)  #保存图片的URL
	#news_id = models.ForeignKey(News)  #与news表外键相互引用
	pictureID = models.IntegerField()  #与News表的中picture_id对应

	def __unicode__(self):
		return str(self.id)

class News(models.Model): #新闻表
	newsType = models.CharField(max_length = 20) #新闻类型
	newsLable = models.CharField(max_length  = 20, blank = True) #新闻label
	newsTitle = models.CharField(max_length = 128)  #新闻标题
	newsContent = models.TextField(max_length = 51200)  #新闻正文
	picture_id = models.IntegerField(blank = True, null=True) #与Picture表对应的pictureID
	browseNumber = models.IntegerField(default = 0) #当前新闻被浏览的次数
	commentNumber = models.IntegerField(default = 0) #评论次数
	likesNumber = models.IntegerField(default = 0) #点赞数
	newsTime = models.DateTimeField(auto_now = True) #新闻生成时间
	newsUrl = models.URLField(max_length = 256) #新闻来源链接

	def __unicode__(self):
		return self.newsTitle

class Comments(models.Model):  #新闻评论表
	user_id = models.IntegerField()   #评论用户ID
	news_id = models.IntegerField()   #对应新闻的ID
	username = models.CharField(max_length=128)   #是哪个用户的评论
	content = models.CharField(max_length = 512)   #评论内容
	content_time = models.DateTimeField(auto_now = True) #自动保存时间auto_now =True，评论的时间
	comment_parent_id = models.IntegerField(default = 0)  # 为了评论的嵌套，未实现该功能

	def __unicode__(self):
		return str(self.id)





