from django import forms
from .models import ScoutReport, Player, Match, Club, Country
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class ScoutRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None

    def save(self, commit=True):
        user = super(ScoutRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            group = Group.objects.get(name="Scout")
            user.groups.add(group)

        return user


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            "name",
            "birth_date",
            "height",
            "photo",
            "nationality",
            "position",
            "club",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "input_field"}),
            "birth_date": forms.DateInput(
                attrs={"class": "input_field", "type": "date"}
            ),
            "height": forms.NumberInput(attrs={"class": "input_field"}),
            "photo": forms.FileInput(attrs={"class": "input_field"}),
            "nationality": forms.Select(attrs={"class": "input_field"}),
            "position": forms.TextInput(attrs={"class": "input_field"}),
            "club": forms.Select(attrs={"class": "input_field"}),
        }

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)

        self.fields["nationality"].queryset = Country.objects.all()
        self.fields["club"].queryset = Club.objects.all()


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

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating is not None and (rating <= 0 or rating > 10):
            raise forms.ValidationError("The rating must be between 0 and 10.")

        return rating

    def clean_match(self):
        match = self.cleaned_data.get("match")
        player = self.cleaned_data.get("player")

        if match.home_club != player.club and match.away_club != player.club:
            raise forms.ValidationError(
                "Player club does not match clubs from the match."
            )

        return match

    def clean_minutes_played(self):
        minutes_played = self.cleaned_data.get("minutes_played")

        if minutes_played < 0:
            raise forms.ValidationError("The number of minutes must be greater than 0.")

        return minutes_played


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
