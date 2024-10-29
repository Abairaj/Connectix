from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User

from .serializers import UserLoginSerializer, UserSerializer
from .utils import (get_redis_client, send_magic_link_email,
                    send_password_reset_email)

token_generator = PasswordResetTokenGenerator()

redis_client = get_redis_client()


class RegisterUserView(APIView):
    permission_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = ()

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)}
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class MagicLinkRequestView(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email)
        if user.exists():
            token = token_generator.make_token(email)
            redis_client.set(token, email, ex=86400)
            send_magic_link_email(
                email, f"http://localhost:3000/magic-link-login?token={token}"
            )
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MagicLinkLoginView(APIView):
    permission_classes = ()

    def post(self, request):
        token = request.data.get("token")
        email = redis_client.get(token)
        redis_client.delete(token)
        if email:
            user = authenticate(
                email=email, backend="django.contrib.auth.backends.ModelBackend"
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"refresh": str(refresh), "access": str(refresh.access_token)}
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = ()

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        token = token_generator.make_token(user)
        redis_client.set(token, email, ex=86400)
        if user:
            # todo have to give correct link to frontend
            send_password_reset_email(
                email, f"http://localhost:3000/reset-password?token={token}"
            )
            return Response(status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_400_BAD_REQUEST, message="User with this Email not found"
        )


# todo check whether the password is same as old password
#  blacklist the old token after changing password


class ResetPasswordView(APIView):
    permission_classes = ()

    def post(self, request):
        token = request.data.get("token")
        password = request.data.get("password")
        email = redis_client.get(token).decode()
        redis_client.delete(token)
        if email:
            user = User.objects.get(email=email)
            if user:
                user.set_password(password)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
