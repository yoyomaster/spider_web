#encoding: utf-8
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import UserProfile, Picture, News, Comments
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import UserForm,ProfileForm
import MySQLdb
from django.db import connection,transaction

def index(request):
	news_list = []
	# news_list = News.objects.all()[0:10]
	news_list1 = News.objects.order_by('?')
	#print news_list  # for debug
	for one_news in news_list1:
		picRecord =Picture.objects.filter( pictureID = one_news.picture_id )
		picUrl = ""
		if picRecord:
			picUrl = picRecord[0].picture
		newsList={}
		newsList['title'] = one_news.newsTitle
		newsList['abstract'] = one_news.newsAbstract
		newsList['picUrl'] = picUrl
		newsList['time'] = one_news.newsTime
		newsList['browseNumber'] = one_news.browseNumber
		newsList['likesNumber'] = one_news.likesNumber
		newsList['commentNumber'] = one_news.commentNumber
		newsList['newsUrl'] = one_news.newsUrl
		newsList['id'] = one_news.id
		news_list.append(newsList)
		print picUrl
		print "------------------------------------------------------------------"

	return render(request, 'app/base.html', {'news_list':news_list})

def showNews(request, newsID):
	#News表浏览数+1
	news = News.objects.get(id = newsID)
	news.browseNumber = news.browseNumber +1
	news.save()

	picture  =  Picture.objects.filter( pictureID = news.picture_id)
	comment = Comments.objects.filter(news_id = newsID).order_by("-content_time")
	return render(request, 'app/newsDetails.html', {'news':news,'picture':picture,'comment':comment})


def register(request):
	registered = False
	errors=[]
	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = ProfileForm(data = request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit = False)
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user

			if 'userImage' in request.FILES:
				profile.userImage = request.FILES['userImage']

			profile.save()
			registered = True
		else:
			errors.append(user_form.errors)
			errors.append(profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = ProfileForm()
	return render(request, 'app/register.html', {'user_form':user_form, 'profile_form':profile_form, 'errors':errors,'registered':registered})



def user_login(request):
	errors=[]
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username = username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				user_m = User.objects.get(username = username)

				#用户登陆次数+1
				profile_m = UserProfile.objects.get(user = user_m)
				profile_m.loginCount = profile_m.loginCount+1
				profile_m.save()

				return HttpResponseRedirect('/app/')
			else:
				errors.append('您的账号暂时无法使用')
				return render(request,'app/login.html',{'errors':errors})
		else:
			errors.append('用户名或密码错误，请重试')
			return render(request,'app/login.html',{'errors':errors})
	else:
		return render(request, 'app/login.html',{})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/app/')


def personal(request):
	res = {}
	comment_res=[]
	cursor = connection.cursor()
	news_list=[] #返回被评论过的新闻列表
	user_id =  request.user.id
	profile = UserProfile.objects.get(user = request.user)
	res['userImage'] = profile.userImage
	print profile.userImage
	if str(res['userImage']) [0] != '/':  #头像
		res['userImage'] = '/'+ str(res['userImage'])

	#.objects.raw('select n.* from app_comments c,app_news n where c.user_id = 11 and n.id = c.news_id')
	cursor.execute('select distinct n.id,n.newsTitle from app_comments c,app_news n where c.user_id = %s and n.id = c.news_id',  [request.user.id])
	sql = cursor.fetchall()
	for sql_res in sql:
		tmp={}
		tmp['url'] = "/app/news/" +str(sql_res[0])
		tmp['title']  =sql_res[1]
		comment_res.append(tmp)

	res['news_list'] = comment_res
	return render(request,'app/personal.html',res)


def comment(request,userID, newsID):
	str1 = request.META['HTTP_REFERER']
	pageStr = str1[str1.find('/app'):]  
	username = User.objects.get(id = userID)
	print userID
	print newsID
	#更新news表的评论数
	news_to_update = News.objects.get(id = newsID)
	news_to_update.commentNumber = news_to_update.commentNumber+1
	news_to_update.save()

	#更新userProfile表的评论数
	user_m = User.objects.get(id = userID)
	profile_m = UserProfile.objects.get(user = user_m)
	profile_m.commentCount = profile_m.commentCount+1
	profile_m.save()

	print pageStr
	print request.POST['content']
	Comments.objects.create(user_id = userID, news_id=newsID,username = username,content=request.POST['content'])
	return HttpResponseRedirect(pageStr)


def modifyPassword(request):
	res = False
	errors=''
	if request.method == "POST":
		if len(request.POST['old_password']) > 0 and len(request.POST['passwrod1']) > 0 and len(request.POST['passwrod2']) > 0:

			user = User.objects.get(username = request.user.username)
			if request.POST['passwrod1'] == request.POST['passwrod2']:
				user_m = User.objects.get(username = request.user.username)
 				if authenticate(username = request.user.username, password = request.POST['old_password']):
					user_m.set_password(request.POST['passwrod1'])
					user_m.save()
					res = True
					return render(request, "app/modifyPassword.html",{'errors':errors,'res':res})
				else:
					errors="密码错误，请重试"
					return render(request, "app/modifyPassword.html",{'errors':errors})
			else:
				errors="输入的两次密码不同"
				return render(request, "app/modifyPassword.html",{'errors':errors})
		else:
			errors="密码不能为空"
			return render(request, "app/modifyPassword.html",{'errors':errors})
	else:
		return render(request, "app/modifyPassword.html",{})
			




