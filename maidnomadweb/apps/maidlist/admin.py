from apps.stafflist.admin import StaffProfileAdmin
from django.contrib import admin

from .models import MaidProfile
from .resources import MaidProfileResource


@admin.register(MaidProfile)
class MaidProfileAdmin(StaffProfileAdmin):
    # for import-export
    resource_class = MaidProfileResource
