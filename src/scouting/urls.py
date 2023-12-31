from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("create-scout-report", views.create_scout_report, name="create_scout_report"),
    path("view-reports", views.view_reports, name="view_reports"),
    path("add-match", views.add_match, name="add_match"),
    path("delete-report/<int:report_id>/", views.delete_report, name="delete_report"),
    path("players/<slug:slug>", views.player_details, name="player_details"),
]
