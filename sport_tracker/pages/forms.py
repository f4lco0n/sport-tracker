from django import forms
from game.models import SportGame
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


class RenewMatchForm(forms.Form):
    def __init__(self, author, opponent, *args, **kwargs):
        super(RenewMatchForm, self).__init__(*args, **kwargs)
        pk_list = [author.id, opponent.id]
        self.fields["winner"].queryset = User.objects.filter(pk__in=pk_list)

    result = forms.CharField(help_text='Wynik powinien być przedzielony ":"', label="Wynik", widget=forms.TextInput(
        attrs={"rows": 1, "class": "form-control", "placeholder": "0:0"}))
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


class StatisticExportForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Data od")
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Data do")
