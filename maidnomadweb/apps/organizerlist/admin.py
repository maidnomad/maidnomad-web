from apps.stafflist.admin import StaffProfileAdmin
from django.contrib import admin

from .models import OrganizerProfile
from .resources import OrganizerProfileResource


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(StaffProfileAdmin):
    # for import-export
    resource_class = OrganizerProfileResource
