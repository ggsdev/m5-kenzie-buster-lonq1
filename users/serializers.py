from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from movies.serializers import MovieSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message="username already taken."),
        ]
    )
    email = serializers.CharField(
        max_length=127,
        validators=[
            UniqueValidator(User.objects.all(), message="email already registered."),
        ],
    )
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, data):
        if data["is_employee"]:
            return User.objects.create_superuser(**data)

        return User.objects.create_user(**data)

    def update(self, instance: User, validated_data: dict):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance
