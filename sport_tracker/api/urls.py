from django.urls import path, include
from .views import sport_game, match

games_patterns = [
    path('', sport_game.GameSportList.as_view(), name='game_sport_list'),
]

match_patterns = [
    path('', match.MatchList.as_view(), name='match_list'),
]


urlpatterns = [
    path('games/', include(games_patterns)),
    path('matches/', include(match_patterns))
]
