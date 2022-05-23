from rest_framework import serializers, status


class MatchSerializer(serializers.Serializer):
    game = serializers.CharField(required=False, allow_null=True)
    comment = serializers.CharField(max_length=120)
    result = serializers.CharField(max_length=10)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
