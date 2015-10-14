#encoding: utf-8
from django.conf.urls import patterns, include, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index' ),
    url(r'^news/(?P<newsID>[\d]+)$', views.showNews, name = 'showNews'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^logout/$', views.user_logout, name = 'logout'),
    url(r'^personal/$', views.personal, name= 'personal'),
    url(r'^comment/(?P<userID>\d+?)/(?P<newsID>\d+?)/$', views.comment, name='comment'),
#测试模板页面
    url(r'^base/$',views.test_base, name = 'test_base'),
)
