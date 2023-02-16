from rest_framework import serializers
from .models import Movie, Ratings, MovieOrder


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default=None)
    rating = serializers.ChoiceField(choices=Ratings.choices, default=Ratings.G)
    synopsis = serializers.CharField(default=None)
    added_by = serializers.EmailField(source="user.email", read_only=True)

    def create(self, data):
        return Movie.objects.create(**data)


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    title = serializers.CharField(source="movie.title", read_only=True)
    buyed_by = serializers.CharField(source="orderer.email", read_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)

    def create(self, data):
        return MovieOrder.objects.create(**data)
