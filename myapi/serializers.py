from rest_framework import serializers
from .models import Hero


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'alias')


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=200, label='密码')


class DeleteManySerializer(serializers.Serializer):
    id = serializers.ListField(
        child=serializers.Field()
    )
