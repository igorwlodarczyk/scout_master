from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import is_user_in_group
from .forms import ScoutReportForm, MatchForm
from .models import ScoutReport, Player

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
    reports = ScoutReport.objects.all().filter(scout_name=user)
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
    player_reports = ScoutReport.objects.all().filter(player=player)
    context = {"player": player, "reports": player_reports}
    return render(request, "scouting/player_details.html", context)


@login_required(login_url="/login/")
def edit_report(request, report_id):
    # TODO fix form rendering
    report = get_object_or_404(ScoutReport, id=report_id)
    form = ScoutReportForm(request.POST or None, instance=report)
    if form.is_valid():
        form.save()
        return redirect("view_reports")

    return render(
        request, "scouting/edit_report.html", {"form": form, "report": report}
    )
