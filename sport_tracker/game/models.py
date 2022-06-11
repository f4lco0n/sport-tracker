from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class SportGame(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nazwa aktywności")

    def __str__(self):
        return '{}'.format(self.name)


class Match(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Autor meczu',
        on_delete=models.CASCADE,
        related_name="author"
    )
    game = models.ForeignKey(SportGame,
                             verbose_name="Gra",
                             on_delete=models.SET_NULL,
                             related_name="games",
                             null=True,
                             blank=True)
    result = models.CharField(max_length=10,
                              verbose_name="Wynik",
                              null=True,
                              blank=True
                              )
    opponent = models.ForeignKey(
        User, verbose_name='Przeciwnik',
        on_delete=models.CASCADE,
        related_name="opponent"
    )
    winner = models.ForeignKey(User, verbose_name="Wygrany", on_delete=models.CASCADE, related_name="match_winner")
    date = models.DateTimeField(default=datetime.now, blank=True)


class Confirmation(models.Model):
    STATUS_PENDING_CONFIRMATION = "Oczekujący zatwierdzenia"
    STATUS_CONFIRMED = "Zatwierdzony"
    STATUS_REJECTED = "Odrzucony"
    match = models.ForeignKey(Match, verbose_name="Mecz",
                              on_delete=models.CASCADE,
                              related_name="matches")
    status = models.CharField(max_length=25,
                              verbose_name="Status")
    comment = models.TextField(default="")
    rejected_by = models.ForeignKey(User, verbose_name="Odrzucony przez", null=True, blank=True,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return 'Gra: {} - Wynik {} - Status: {}'.format(self.match.game.name, self.match.result, self.status)


class ConfirmationMessage(models.Model):
    confirmation = models.ForeignKey(Confirmation, on_delete=models.CASCADE, verbose_name="Potwierdzenie",
                                     related_name="messages")
    message = models.TextField(verbose_name="Wiadomość", blank=True, max_length=1000, default='')
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.CASCADE, related_name="user_comments")
    date = models.DateTimeField(default=datetime.now, blank=True)
