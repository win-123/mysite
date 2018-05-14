from django.contrib import admin
from .models import ApproveCount, ApproveRecord

# Register your models here.

@admin.register(ApproveCount)
class ApproveCountAdmin(admin.ModelAdmin):
	list_display = ("content_type", "object_id", "approve_num", )


@admin.register(ApproveRecord)
class ApproveRecordAdmin(admin.ModelAdmin):
	list_display = ("content_type", "object_id", "user", "approve_time", )

