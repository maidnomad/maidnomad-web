from apps.stafflist.urls import get_staff_profile_urlpatterns

from . import views

urlpatterns = []
urlpatterns += get_staff_profile_urlpatterns(views.OrganizerProfileViewSet)
