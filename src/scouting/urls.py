from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("create-scout-report", views.create_scout_report, name="create_scout_report"),
    path("view-reports", views.view_reports, name="view_reports"),
    path("add-match", views.add_match, name="add_match"),
]
