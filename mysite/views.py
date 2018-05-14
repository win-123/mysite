from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse

from read_statistics.utils import get_seven_days_read_data
from read_statistics.utils import get_yesterday_hot_data
from read_statistics.utils import get_today_hot_data
from read_statistics.utils import get_seven_days_hot_data
from blog.models import Blog
from .forms import LoginForm
from .forms import RegisterForm


def home(request):
	"""
	首页信息
	"""
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)

	# 获取7天热门博客缓存数据
	hot_blogs_for_seven_days = cache.get("hot_blogs_for_seven_days")
	if hot_blogs_for_seven_days is None:
		hot_blogs_for_seven_days = get_seven_days_hot_blogs()
		cache.set("hot_blogs_for_seven_days", hot_blogs_for_seven_days, 3600)
	

	context = {}
	context["dates"] = dates
	context["read_nums"] = read_nums
	context["today_hot_data"] = get_today_hot_data(blog_content_type)
	context["yesterday_hot_data"] = get_yesterday_hot_data(blog_content_type)
	context["hot_blogs_for_seven_days"] = hot_blogs_for_seven_days

	return render(request, "home.html", context)


def get_seven_days_hot_blogs():
	"""
	获取7天热门博客数据
	"""
	today  = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects.filter(read_detail__date__lt=today,read_detail__date__gte=date).values("id", "title").annotate(read_num_sum=Sum("read_detail__read_num")).order_by("read_num_sum")

	return blogs[:7]


def signin(request):
	# username = request.POST.get("username", "")
	# password = request.POST.get("password", "")
	# context = {}

	# user = authenticate(request, username=username, password=password)
	# referer = request.META.get("HTTP_REFERER", reverse("home"))

	# if user is not None:
	# 	login(request, user)
	# 	return redirect(referer)

	# else:
	# 	context["msg"] = "用户名或密码错误"

	# 	return render(request, "error.html", context)
	context = {}
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			
			user = login_form.cleaned_data["user"]
			login(request, user)
			return redirect(request.GET.get("from", reverse("home")))

	else:
		login_form = LoginForm()

	context["login_form"] = login_form

	return render(request, "login.html", context)


def signup(request):

	context = {}
	if request.method == "POST":
		reg_form = RegisterForm(request.POST)
		if reg_form.is_valid():
			
			username = reg_form.cleaned_data["username"]
			email = reg_form.cleaned_data["email"]
			password = reg_form.cleaned_data["password"]

			user = User.objects.create_user(username, email, password)
			user.save()

			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect(request.GET.get("from", reverse("home")))

	else:
		reg_form = RegisterForm()

	context["reg_form"] = reg_form

	return render(request, "register.html", context)


def login_for_medal(request):

    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'

    return JsonResponse(data)


def quit(request):
	logout(request)
	return redirect(request.GET.get("form", reverse("home")))


def user_info(request):
	context = {}

	return render(request, "user_info.html", context)

	





