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

def index(request): #主页
	news_list = []
	# news_list = News.objects.all()[0:10]
	news_list1 = News.objects.order_by('?')[:20] #随机排序取前20条记录
	#print news_list  # for debug
	for one_news in news_list1:
		picRecord =Picture.objects.filter( pictureID = one_news.picture_id )
		picUrl = ""
		if picRecord:
			picUrl = picRecord[0].picture #只取一张图片在主页显示
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
		newsList['type'] = one_news.newsType
		news_list.append(newsList) #追加到news_list列表中
		# print picUrl
		# print "------------------------------------------------------------------"

	return render(request, 'app/index.html', {'news_list':news_list})

def showNews(request, newsID): #新闻二级页面
	#News表浏览数+1
	news = News.objects.get(id = newsID)
	news.browseNumber = news.browseNumber +1
	news.save() #保存

	picture  =  Picture.objects.filter( pictureID = news.picture_id)
	comment = Comments.objects.filter(news_id = newsID).order_by("content_time") #评论内容按content_time排序
	return render(request, 'app/newsDetails.html', {'news':news,'picture':picture,'comment':comment})


def register(request): #注册
	registered = False
	errors=[]
	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = ProfileForm(data = request.POST)
		if user_form.is_valid() and profile_form.is_valid(): 
			user = user_form.save(commit = False)
			user.set_password(user.password)  #设置密码
			user.save()
			profile = profile_form.save(commit=False)  #不保存
			profile.user = user

			if 'userImage' in request.FILES:  #判断是否有上传头像
				profile.userImage = request.FILES['userImage']

			profile.save()  #保存
			registered = True
		else:
			errors.append(user_form.errors)
			errors.append(profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = ProfileForm()
	return render(request, 'app/register.html', {'user_form':user_form, 'profile_form':profile_form, 'errors':errors,'registered':registered})



def user_login(request): #登陆
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
	res['userImage'] = profile.userImage #里面保存的是图片的路径
	# print profile.userImage
	if str(res['userImage']) [0] != '/':  #头像
		res['userImage'] = '/'+ str(res['userImage'])

	#.objects.raw('select n.* from app_comments c,app_news n where c.user_id = 11 and n.id = c.news_id')
	# 从数据库中取出该用户评论过的新闻的id和title
	cursor.execute('select distinct n.id,n.newsTitle from app_comments c,app_news n where c.user_id = %s and n.id = c.news_id',  [request.user.id])
	sql = cursor.fetchall()
	for sql_res in sql:
		tmp={}
		tmp['url'] = "/app/news/" +str(sql_res[0])  #保存对应的新闻链接
		tmp['title']  =sql_res[1]
		comment_res.append(tmp)

	res['news_list'] = comment_res
	return render(request,'app/personal.html',res)


def comment(request,userID, newsID):
	str1 = request.META['HTTP_REFERER']  #请求页面的url
	pageStr = str1[str1.find('/app'):]  
	username = User.objects.get(id = userID)
	# print userID
	# print newsID
	#更新news表的评论数
	news_to_update = News.objects.get(id = newsID)
	news_to_update.commentNumber = news_to_update.commentNumber+1
	news_to_update.save()

	#更新userProfile表的评论数
	user_m = User.objects.get(id = userID)
	profile_m = UserProfile.objects.get(user = user_m)
	profile_m.commentCount = profile_m.commentCount+1
	profile_m.save()

	Comments.objects.create(user_id = userID, news_id=newsID,username = username,content=request.POST['content']) #将评论内容保存到数据库
	return HttpResponseRedirect(pageStr) #重定向到原来请求页面


def modifyPassword(request): #更改密码
	res = False
	errors=''
	if request.method == "POST":
		if len(request.POST['old_password']) > 0 and len(request.POST['passwrod1']) > 0 and len(request.POST['passwrod2']) > 0: 

			user = User.objects.get(username = request.user.username)
			if request.POST['passwrod1'] == request.POST['passwrod2']:
				user_m = User.objects.get(username = request.user.username)
 				if authenticate(username = request.user.username, password = request.POST['old_password']): #验证用户名与密码是否匹配
					user_m.set_password(request.POST['passwrod1']) #设置密码
					user_m.save() #保存
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
			

def  contact(request):
	return render(request, "app/contact.html",{})

def  about(request):
	return render(request,"app/about.html",{})


