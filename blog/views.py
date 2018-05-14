from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from mysite.settings import EACH_PAGE_NUMBER
from .models import Blog
from .models import BlogType
from comment.models import Comment
from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read
from comment.forms import CommentForm
from mysite.forms import LoginForm


# Create your views here.

def blog_list(request):
	"""
	博客列表
	"""
	blogs_all_list = Blog.objects.all()
	paginator = Paginator(blogs_all_list, EACH_PAGE_NUMBER)
	page_num = request.GET.get('page', 1)
	page_of_blogs = paginator.get_page(page_num)
	current_page_num = page_of_blogs.number
	page_range = list(range(max(current_page_num -2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2,paginator.num_pages) + 1))

	context = {}
	
	context["page_of_blogs"] = page_of_blogs
	context["blog_types"] = BlogType.objects.all()
	context["page_range"] = page_range
	context["blogs_count"] = Blog.objects.all().count()
	context["blog_dates"] = Blog.objects.dates("create_time", "month", order="DESC")

	return render(request, "blog/blog_list.html", context)

	
def blog_detail(request, blog_pk):
	"""
	博客详情
	"""
	context = {}
	blog = get_object_or_404(Blog, pk=blog_pk)
	read_cookie_key = read_statistics_once_read(request, blog)
	# blog_content_type = ContentType.objects.get_for_model(blog)
	# comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

	context["previous_blog"] = Blog.objects.filter(create_time__gt=blog.create_time).last()
	context["next_blog"] = Blog.objects.filter(create_time__lt=blog.create_time).first()
	# context["blog_dates"] = Blog.objects.dates("create_time", "month", order="DESC")

	context["blog"] = blog
	context["login_form"] = LoginForm()
	
	response = render(request, "blog/blog_detail.html", context)
	response.set_cookie(read_cookie_key, "true", max_age=60)

	return response


def blogs_with_type(request, blog_type_pk):
	"""
	博客类型
	"""
	context = {}
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
	context["blogs"] = Blog.objects.filter(blog_type=blog_type)
	context["blog_type"] = blog_type
	return render(request, "blog/blogs_with_type.html", context)


def blogs_with_date(request, year, month):
	context = {}
	blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
	paginator = Paginator(blogs_all_list, EACH_PAGE_NUMBER)
	page_num = request.GET.get('page', 1)
	page_of_blogs = paginator.get_page(page_num)
	current_page_num = page_of_blogs.number
	page_range = list(range(max(current_page_num -2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2,paginator.num_pages) + 1))

	context["page_of_blogs"] = page_of_blogs
	context["blogs_with_date"] = "%s年%s月" % (year, month)
	context["blog_types"] = BlogType.objects.all()
	context["page_range"] = page_range
	context["blogs_count"] = Blog.objects.all().count()
	context["blog_dates"] = Blog.objects.dates("create_time", "month", order="DESC")

	return render(request, "blog/blogs_with_date.html", context)





