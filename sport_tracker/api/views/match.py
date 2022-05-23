from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import Match
from api.serializers.match_serializer import MatchSerializer


class MatchList(APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        matches = Match.objects.all()

        serializer = MatchSerializer(matches, many=True, context={"request": request})
        return Response(serializer.data)
