from django import forms
from .models import ScoutReport, Player, Match, Club


class ScoutReportForm(forms.ModelForm):
    class Meta:
        model = ScoutReport
        fields = ["player", "match", "rating", "minutes_played", "scout_name"]

        widgets = {
            "player": forms.Select(attrs={"class": "input_field"}),
            "match": forms.Select(attrs={"class": "input_field"}),
            "rating": forms.NumberInput(attrs={"class": "input_field"}),
            "minutes_played": forms.NumberInput(attrs={"class": "input_field"}),
            "scout_name": forms.TextInput(attrs={"class": "input_field"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ScoutReportForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["scout_name"].initial = user.username

        self.fields["player"].queryset = Player.objects.all()
        self.fields["match"].queryset = Match.objects.all()


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["date", "home_club", "away_club", "result"]
        widgets = {
            "date": forms.DateInput(
                attrs={"class": "input_field", "placeholder": "YYYY-MM-DD"}
            ),
            "home_club": forms.Select(attrs={"class": "input_field"}),
            "away_club": forms.Select(attrs={"class": "input_field"}),
            "result": forms.TextInput(attrs={"class": "input_field"}),
        }

        labels = {
            "date": "Date",
            "home_club": "Home club",
            "away_club": "Away club",
            "result": "Result",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["home_club"].queryset = Club.objects.all()
        self.fields["away_club"].queryset = Club.objects.all()
