from django import forms
from game.models import SportGame, Match
from django.contrib.auth.models import User


class MatchForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields["opponent"].queryset = User.objects.exclude(id=user.id)

    game = forms.ModelChoiceField(
        label="Gra",
        queryset=SportGame.objects.all(),
        widget=forms.Select(
            attrs={'placeholder': 'Gra', 'class': 'form-control'}
        )
    )
    result = forms.CharField(help_text='Wynik powinien być przedzielony ":"', label="Wynik", widget=forms.TextInput(
        attrs={"rows": 1, "class": "form-control", "placeholder": "0:0"}))
    opponent = forms.ModelChoiceField(
        label="Przeciwnik",
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"placeholder": "Opponent", "class": "form-control"}
        ))
    winner = forms.ModelChoiceField(
        label="Zwycięzca",
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={"placeholder": "Opponent", "class": "form-control"}
        ))


class ConfirmationMessageForm(forms.Form):
    message = forms.CharField(label="Wiadomości", max_length=1000, widget=forms.Textarea(attrs={
        "rows": 3,
        "cols": 40,
        "class": "form-control"
    }))