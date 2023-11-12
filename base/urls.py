from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-base-survey", views.create_base_survey, name="create_base_survey"),
]