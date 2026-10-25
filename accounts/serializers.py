from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации.

    Поле password помечено write_only — оно не возвращается в ответе.
    Валидатор validate_password требует, чтобы пароль соответствовал
    настройкам AUTH_PASSWORD_VALIDATORS (длина, неочевидность и т.д.).
    create_user вместо create — автоматически хэширует пароль.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Сериализатор входа: логин и пароль."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
