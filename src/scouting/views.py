from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from .forms import ScoutReportForm, MatchForm
from .models import ScoutReport

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


def add_match(request):
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success_page")
    else:
        form = MatchForm()

    return render(request, "scouting/add_match.html", {"form": form})


def view_reports(request):
    user = str(request.user)
    reports = ScoutReport.objects.all().filter(scout_name=user)
    context = {"reports": reports}
    return render(request, "scouting/view_reports.html", context)
