#encoding: utf-8
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from app.models import UserProfile, Picture, News, Comments
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.forms import UserForm,ProfileForm
import MySQLdb

# Create your views here.
# 新闻类型暂时分两种 科技technology， 娱乐entertainment,社会类 society
def index(request):
	# news_list = {}
	# news_list['technology'] = News.objects.filter(newsType =  'technology')
	# news_list['entertainment'] = News.objects.filter(newsType = 'entertainment')
	# news_list['society'] = News.objects.filter(newsType = 'society')

	news_list = News.objects.all()[0:10]
	# news_list = News.objects.order_by('?')[0:2]

	#print news_list  # for debug
	# for x in news_list['technology']:     #for debug
	# 	print x.id
	# 	print '-------------------'
	return render(request, 'app/index.html', {'news_list':news_list})



def showNews(request, newsID):
	# allComment=[]
	news = News.objects.get(id = newsID)
	news.browseNumber = news.browseNumber +1
	news.save()
	#print news      #debug()
	picture  =  Picture.objects.filter( pictureID = news.picture_id)
	#print  picture
	comment = Comments.objects.filter(news_id = newsID).order_by("-content_time")
	# print newsID
	# print comment
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
			print request.FILES

			# if request.FILES['userImage']:
			if 'userImage' in request.FILES:
				print 'has a Picture 1'
				profile.userImage = request.FILES['userImage']


			profile.save()
			registered = True
			# HttpResponseRedirect('app/')
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
	print request.user
	print type(request.user)
	profile = UserProfile.objects.get(user = request.user)
	res['userImage'] = profile.userImage
	print profile.userImage
	if str(res['userImage']) [0] != '/':
		res['userImage'] = '/'+ str(res['userImage'])

	return render(request,'app/personal.html',res)


def comment(request,userID, newsID):
	str1 = request.META['HTTP_REFERER']
	pageStr = str1[str1.find('/app'):]
	username = User.objects.get(id = userID)
	news_to_update = News.objects.get(id = newsID)
	news_to_update.commentNumber = news_to_update.commentNumber+1
	news_to_update.save()
	print pageStr
	print request.POST['content']
	Comments.objects.create(user_id = userID, news_id=newsID,username = username,content=request.POST['content'])
	return HttpResponseRedirect(pageStr)


# def test(request):
# 	ua = request.META
# 	for x in ua:
# 		print x
# 		print '/n'
# 	return HttpResponse('your browser is %s'  %ua)
			
#测试模板页面
def test_base(request):
	return render(request, 'base.html',{})



