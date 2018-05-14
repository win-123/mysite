from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


# Create your views here.

def update_comment(request):
	"""
	评论内容处理
	"""

	context = {}
	referer = request.META.get("HTTP_REFERER", reverse("home"))
	comment_form = CommentForm(request.POST, user=request.user)
	data = {}
	if comment_form.is_valid():
		comment = Comment()
		comment.user = comment_form.cleaned_data["user"]
		comment.text = comment_form.cleaned_data["text"]
		comment.content_object = comment_form.cleaned_data["content_object"]

		parent = comment_form.cleaned_data["parent"]
		if not parent is None:
			comment.root = parent.root if not parent.root is None else parent
			comment.parent = parent
			comment.reply_to = parent.user
		comment.save()

		data["status"] = "SUCCESS"
		data["username"] = comment.user.username
		data["comment_time"] = comment.comment_time.timestamp()
		data["text"] = comment.text
		if not parent is None:
			data["reply_to"] = comment.reply_to.username

		else:
			data["reply_to"] = ""

		data["pk"] = comment.pk
		data["root_pk"] = comment.root.pk if not comment.root is None else ""
		# return redirect(referer)

	else:
		# context["msg"] = comment_form.errors
		# context["redirect_to"] = referer
		# return render(request, "error.html", context)
		data["status"] = "ERROR"
		data["msg"] = list(comment_form.errors.values())[0][0]

	return JsonResponse(data)
	







