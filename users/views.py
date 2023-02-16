from rest_framework.views import APIView, status, Request, Response
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsResourceOwnerOrEmployeePermission
from .models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsResourceOwnerOrEmployeePermission]

    def get(self, request: Request, user_id: int) -> Response:
        user_object = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_object)
        serializer = UserSerializer(user_object)

        return Response(serializer.data)

    def patch(self, request: Request, user_id: int) -> Response:
        user_object = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user_object)

        serializer = UserSerializer(user_object, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
