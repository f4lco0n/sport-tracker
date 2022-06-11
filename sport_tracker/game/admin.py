from django.contrib import admin
from .models import SportGame, Match, Confirmation, ConfirmationMessage


@admin.register(SportGame)
class SportGameAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "game", "result", "opponent", "winner", "date")


@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = (
        "id", "get_author", "get_match_name", "get_match_result", "get_opponent", "status", "comment", "rejected_by")

    def get_author(self, obj):
        return obj.match.author.username

    def get_match_name(self, obj):
        return obj.match.game.name

    def get_match_result(self, obj):
        return obj.match.result

    def get_opponent(self, obj):
        return obj.match.opponent.username

    get_author.short_description = "Autor"
    get_match_name.short_description = "Gra"
    get_match_result.short_description = "Wynik"
    get_opponent.short_description = "Przeciwnik"


@admin.register(ConfirmationMessage)
class ConfirmationMessageAdmin(admin.ModelAdmin):
    list_display = ("confirmation", "message", "author", "date")
