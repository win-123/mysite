from django.contrib import admin
from .models import Comment

# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "content_object", "comment_time", "text", "user", "root", "parent", )

