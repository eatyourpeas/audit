from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-base-survey", views.create_base_survey, name="create_base_survey"),
    path("base-survey/<int:survey_id>/delete", views.delete_base_survey, name="delete_base_survey"),
    path("base-survey/<int:survey_id>/edit", views.edit_base_survey, name="edit_base_survey"),
]