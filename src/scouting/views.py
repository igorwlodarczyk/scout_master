from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import is_user_in_group
from .forms import ScoutReportForm, MatchForm, PlayerForm, ScoutRegistrationForm
from .models import ScoutReport, Player
from .decorators import group_required

# Create your views here.


@login_required(login_url="/login/")
def index(request):
    return render(request, "scouting/index.html")


@login_required(login_url="/login/")
def create_scout_report(request):
    if request.method == "POST":
        form = ScoutReportForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = ScoutReportForm(user=request.user)

    return render(request, "scouting/create_report.html", {"form": form})


@login_required(login_url="/login/")
def add_match(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = MatchForm()

    return render(request, "scouting/add_match.html", {"form": form})


@login_required(login_url="/login/")
def view_reports(request):
    groups = request.user.groups.all()
    user = str(request.user)
    reports = ScoutReport.objects.all()
    context = {
        "reports": reports,
        "user": user,
        "sports_director": is_user_in_group(groups, "Sports_director"),
    }
    return render(request, "scouting/view_reports.html", context)


@login_required(login_url="/login/")
def delete_report(request, report_id):
    report = get_object_or_404(ScoutReport, id=report_id)
    report.delete()
    return redirect("view_reports")


@login_required(login_url="/login/")
def player_details(request, slug):
    player = get_object_or_404(Player, slug=slug)
    player_reports = (
        ScoutReport.objects.all().filter(player=player).order_by("-match__date")
    )
    context = {"player": player, "reports": player_reports}
    return render(request, "scouting/player_details.html", context)


@login_required(login_url="/login/")
def edit_report(request, report_id):
    report = get_object_or_404(ScoutReport, id=report_id)
    form = ScoutReportForm(request.POST or None, instance=report)
    if form.is_valid():
        form.save()
        return redirect("view_reports")

    return render(
        request, "scouting/edit_report.html", {"form": form, "report": report}
    )


@login_required(login_url="/login/")
def view_players(request):
    players = Player.objects.all()
    context = {"players": players}
    return render(request, "scouting/view_players.html", context)


@login_required(login_url="/login/")
def delete_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player.delete()
    return redirect("view_players")


@login_required(login_url="/login/")
def edit_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return redirect("view_players")
    else:
        form = PlayerForm(instance=player)

    return render(
        request, "scouting/edit_player.html", {"form": form, "player": player}
    )


@login_required(login_url="/login/")
def add_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("view_players")
    else:
        form = PlayerForm()

    return render(request, "scouting/add_player.html", {"form": form})


@login_required(login_url="/login/")
def success_page(request):
    return render(request, "scouting/success_page.html")


@login_required(login_url="/login/")
@group_required("Sports_director")
def add_scout(request):
    if request.method == "POST":
        form = ScoutRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = ScoutRegistrationForm()
    return render(request, "scouting/add_scout.html", {"form": form})


@login_required(login_url="/login/")
def access_denied(request):
    return render(request, "scouting/access_denied.html")
