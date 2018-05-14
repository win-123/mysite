from django.contrib import admin
from .models import Blog, BlogType


# Register your models here.

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
	list_display = ("id", "type_name",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ("title", "blog_type", "author", "get_read_num", "content", "create_time", )



