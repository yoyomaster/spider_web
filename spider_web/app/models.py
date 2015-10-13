#encoding: utf-8
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	userGrade = models.IntegerField(default = 1)
	userImage = models.ImageField(upload_to = 'user_image', blank = True)
	loginCount = models.IntegerField(default = 1)
	lastLogin = models.DateTimeField(auto_now = True)
	likeCount = models.IntegerField(default = 0)
	commentCount = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.user.username


class Picture(models.Model):
#	picture = models.ImageField(upload_to = 'news_images', blank = True)
	picture = models.CharField(max_length = 128)
	#news_id = models.ForeignKey(News)  #与news表外键相互引用
	newsID = models.IntegerField()

	def __unicode__(self):
		return str(self.id)

class News(models.Model):
	newsType = models.CharField(max_length = 20)
	newsLable = models.CharField(max_length  = 20, blank = True)
	newsTitle = models.CharField(max_length = 128)
	newsContent = models.TextField(max_length = 51200)
	picture_id = models.IntegerField(blank = True, null=True)

	def __unicode__(self):
		return self.newsTitle

class Comments(models.Model):
	user_id = models.ForeignKey(User)
	news_id = models.ForeignKey(News)
	content = models.CharField(max_length = 512)
	content_time = models.DateTimeField( ) #自动保存时间auto_time =True
	comment_parent_id = models.IntegerField()

	def __unicode__(self):
		return str(self.id)





