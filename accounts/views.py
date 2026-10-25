from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    """POST — регистрация нового пользователя.

    authentication_classes = [] и permission_classes = [] отключают проверку токена,
    иначе аноним не смог бы зарегистрироваться.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(request=RegisterSerializer, responses={201: dict})
    def post(self, request):
        """Создаёт пользователя и возвращает его токен."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Токен создаётся один раз и переиспользуется при повторных обращениях
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"username": user.username, "token": token.key},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST — вход по логину и паролю.

    Аутентификация и разрешения отключены: эндпоинт должен быть доступен анонимно.
    """

    authentication_classes = []
    permission_classes = []

    @extend_schema(request=LoginSerializer, responses={200: dict})
    def post(self, request):
        """Проверяет учётные данные и возвращает токен.

        authenticate() возвращает None при неверных данных — в этом ответе
        намеренно не уточняется, какое именно поле неверно (не раскрываем существование аккаунта).
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Неверный логин или пароль"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
