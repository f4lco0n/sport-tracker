from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import SportGame
from api.serializers.sport_game_serializer import SportGameSerializer


class GameSportList(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        games = SportGame.objects.all()

        serializer = SportGameSerializer(games, many=True, context={"request": request})
        return Response(serializer.data)
