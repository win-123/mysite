from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum
from read_statistics.models import ReadNumExtendMethod
from read_statistics.models import ReadDetail


# Create your models here.
class Blog(models.Model, ReadNumExtendMethod):
	title = models.CharField(max_length=60)
	blog_type = models.ForeignKey("BlogType", on_delete=models.CASCADE)
	content = RichTextUploadingField()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	read_detail = GenericRelation(ReadDetail)
	
	create_time = models.DateTimeField(auto_now_add=True)
	last_update_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "<Blog:%s>" % self.title

	class Meta:
		ordering = ["-create_time"]


class BlogType(models.Model):
	type_name = models.CharField(max_length=20)

	def __str__(self):
		return self.type_name





