from django.urls import path

from . import views

urlpatterns = [
    path("", views.staticpage("top"), name="top"),
    path("information/for_maidcafe_info", views.staticpage("for_maidcafe_info"), name="for_maidcafe_info"),
    path("information/akihabara_nomad_maid", views.staticpage("akihabara_nomad_maid"), name="akihabara_nomad_maid"),
    path("organization", views.staticpage("organization"), name="organization"),
]
