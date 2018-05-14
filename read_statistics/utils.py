import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum
from .models import ReadDetail


def read_statistics_once_read(request, obj):
	
	ct = ContentType.objects.get_for_model(obj)
	key = "%s_%s_read" % (ct.model, obj.pk)

	if not request.COOKIES.get(key):
	
		read_num, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)

		read_num.read_num += 1
		read_num.save()

		date = timezone.now().date()
		read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
	
		read_detail.read_num += 1
		read_detail.save()

	return key


def get_seven_days_read_data(content_type):
	today = timezone.now().date()
	read_nums = []
	dates = []
	
	for i in range(7, 0, -1):
		date = today - datetime.timedelta(days=i)
		dates.append(date.strftime("%m/%d"))
		read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
		result = read_detail.aggregate(read_num_sum=Sum("read_num"))
		read_nums.append(result["read_num_sum"] or 0)

	return  dates, read_nums


def get_today_hot_data(content_type):
	today  = timezone.now().date()
	read_detail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("-read_num")

	return read_detail[:7]


def get_yesterday_hot_data(content_type):
	today  = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)

	read_detail = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by("-read_num")
	
	return read_detail[:7]


def get_seven_days_hot_data(content_type):
	today  = timezone.now().date()
	date = today - datetime.timedelta(days=7)

	read_detail = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gte=date).values("content_type", "object_id").annotate(read_num_sum=Sum("read_num")).order_by("-read_num")
	
	return read_detail[:7]








