from rest_framework import serializers, status


class SportGameSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
