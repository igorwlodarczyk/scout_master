from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-scout-report", views.create_scout_report, name="create_scout_report"),
    path("view-reports", views.view_reports, name="view_reports"),
    path("add-match", views.add_match, name="add_match"),
    path("delete-report/<int:report_id>/", views.delete_report, name="delete_report"),
    path("players/<slug:slug>", views.player_details, name="player_details"),
    path("edit-report/<int:report_id>/", views.edit_report, name="edit_report"),
    path("view-players", views.view_players, name="view_players"),
    path("delete-player/<int:player_id>/", views.delete_player, name="delete_player"),
    path("edit-player/<int:player_id>/", views.edit_player, name="edit_player"),
    path("add-player", views.add_player, name="add_player"),
    path("success", views.success_page, name="success_page"),
    path("add-scout", views.add_scout, name="add_scout"),
    path("access-denied", views.access_denied, name="access_denied"),
]
