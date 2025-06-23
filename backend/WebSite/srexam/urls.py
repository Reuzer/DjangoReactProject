from django.urls import path
from . import views

urlpatterns = [
    path("srexam/", views.srexam_list, name="srexam_list"),
]
