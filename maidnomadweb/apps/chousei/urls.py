from django.urls import path

from . import views

urlpatterns = [
    path("<str:key>", views.view, name="view"),
    path("<str:key>/add", views.add, name="add"),
    path("<str:key>/edit/<int:person_id>", views.edit, name="edit"),
]
