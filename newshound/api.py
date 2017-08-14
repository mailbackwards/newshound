from rest_framework import serializers, viewsets

from .models import Dog


class DogSerializer(serializers.ModelSerializer):
    breeds = serializers.StringRelatedField(many=True)

    class Meta:
        model = Dog
        fields = '__all__'


class DogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This view powers the admin AJAX "Trending dogs" view.
    """
    serializer_class = DogSerializer
    queryset = Dog.trending.all()

dog_api_view = DogViewSet.as_view({'get': 'list'})
