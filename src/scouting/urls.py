from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("create-scout-report", views.create_scout_report, name="create_scout_report"),
]
