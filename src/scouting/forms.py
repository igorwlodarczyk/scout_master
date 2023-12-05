from django import forms
from .models import ScoutReport, Player, Match


class ScoutReportForm(forms.ModelForm):
    class Meta:
        model = ScoutReport
        fields = ["player", "match", "rating", "minutes_played", "scout_name"]

    def __init__(self, *args, **kwargs):
        # Pobierz użytkownika z kontekstu formularza
        user = kwargs.pop("user", None)
        super(ScoutReportForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["scout_name"].initial = user.username

        self.fields["player"].queryset = Player.objects.all()
        self.fields["match"].queryset = Match.objects.all()
