from rest_framework.views import APIView, status, Request, Response
from .serializers import MovieSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployeePermission
from .models import Movie
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeePermission]

    def get(self, request) -> Response:
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeePermission]

    def get(self, _, movie_id) -> Response:
        movie_object = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie_object)

        return Response(serializer.data)

    def delete(self, _, movie_id) -> Response:
        movie_object = get_object_or_404(Movie, id=movie_id)
        movie_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie_object = get_object_or_404(Movie, id=movie_id)
        serializer.save(orderer=request.user, movie=movie_object)
        return Response(serializer.data, status.HTTP_201_CREATED)
