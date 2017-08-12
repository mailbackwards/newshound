from rest_framework import serializers
from .models import Dog


class DogSerializer(serializers.ModelSerializer):
    breeds = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dog
        fields = '__all__'
