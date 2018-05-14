from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import ApproveCount
from ..models import ApproveRecord


register = template.Library()


@register.simple_tag
def get_approve_count(obj):
	content_type = ContentType.objects.get_for_model(obj)
	approve_count, created =  ApproveCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
	return approve_count.approve_num


@register.simple_tag(takes_context=True)
def get_approve_status(context, obj):
	content_type = ContentType.objects.get_for_model(obj)
	user = context["user"]
	if not user.is_authenticated:
		return ""
	if ApproveRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():

		return "active"
	else:
		return ""


@register.simple_tag
def get_content_type(obj):
	content_type = ContentType.objects.get_for_model(obj)

	return content_type.model

