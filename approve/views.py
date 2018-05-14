from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist

from .models import ApproveCount, ApproveRecord

# Create your views here.

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def SuccessResponse(approve_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['approve_num'] = approve_num
    return JsonResponse(data)


def approve_change(request):

	"""
	点赞操作相关
	"""

	# 验证用户是否登录
	user = request.user
	content_type = request.GET.get("content_type")
	object_id = request.GET.get("object_id")
	is_approved = request.GET.get("is_approved")
	if not user.is_authenticated:
		return ErrorResponse(400, 'you were not login')

	try:
		content_type = ContentType.objects.get(model=content_type)
		model_class = content_type.model_class()
		model_obj = model_class.objects.get(pk=object_id)
	except ObjectDoesNotExist:
		return ErrorResponse(401, "object is not exist")


	if is_approved == "true":
		approve_record, created = ApproveRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)

		if created:
			approve_count, created = ApproveCount.objects.get_or_create(content_type=content_type, object_id=object_id)
			approve_count.approve_num += 1
			approve_count.save()

			return SuccessResponse(approve_count.approve_num)
		else:
			return ErrorResponse(402, 'you were liked')

	else:
		if ApproveRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
			approve_record = ApproveRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
			approve_record.delete()

			approve_count, created = ApproveCount.objects.get_or_create(content_type=content_type, object_id=object_id)

			if not created:
				approve_count.approve_num -= 1
				approve_count.save()

				return SuccessResponse(approve_count.approve_num)
			else:
				return ErrorResponse(404, "data error")
		else:
			 # 没有点赞过，不能取消
			return ErrorResponse(403, "还没点赞")






