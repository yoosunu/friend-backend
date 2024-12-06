from datetime import datetime, timezone, timedelta
import requests
from django.conf import settings
from config.settings import JWT_SECRET, JWT_SECRET_RF
from django.contrib.auth import authenticate, login, logout
import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound, AuthenticationFailed
from .serializers import (
    PrivateUserSerializer,
    PublicUserSerializer,
    ClassicUserSerializer,
)
from .models import User


# Create your views here.
class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = PrivateUserSerializer(updated_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = ClassicUserSerializer(
            users,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        password = request.data.get("password")
        if not password:  # you can add more conditions of password here.
            raise ParseError("password is required.")
        serializer = PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            serializer = PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye!"})


class SignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if not username or not password or not email:
            raise ParseError("All fields are required.")

        if User.objects.filter(username=username).exists():
            raise ParseError("Username already exists.")

        if User.objects.filter(email=email).exists():
            raise ParseError("Email already exists.")

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            user.save()
            login(request, user)
            return Response({"ok": "Signed Up!"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Username or Email is already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                f"https://github.com/login/oauth/access_token",
                headers={
                    "Accept": "application/json",
                },
                data={
                    "code": code,
                    "client_id": "Ov23liEyST7si3OeL9D7",
                    "client_secret": settings.GH_SECRET,
                },
            )

            access_token = access_token.json().get("access_token")

            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_data = user_data.json()

            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_emails = user_emails.json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=user_emails[0]["email"],
                    name=user_data.get("name"),
                    profile_image=user_data.get("avatar_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "d61bd1307b18eb8a40650bfed90a8131",
                    "redirect_uri": "http://apot.pro/social/kakao",
                    "code": code,
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(username=profile.get("nickname"))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=profile.get("nickname"),
                    profile_image=profile.get("profile.image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            access_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
            access_token = jwt.encode(
                {
                    "pk": user.pk,
                    "exp": access_token_expiration,
                },
                JWT_SECRET,
                algorithm="HS256",
            )

            refresh_token_expiration = datetime.now(timezone.utc) + timedelta(days=30)
            refresh_token = jwt.encode(
                {
                    "pk": user.pk,
                    "exp": refresh_token_expiration,
                },
                JWT_SECRET,
                algorithm="HS256",
            )
            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )
        else:
            return Response({"error": "wrong information"})


class RefreshAT(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        try:
            decoded = jwt.decode(refresh_token, JWT_SECRET_RF, algorithms="HS256")
            pk = decoded.get("pk")
            if not pk:
                raise AuthenticationFailed("invalid refresh token")

            user = User.objects.get(pk=pk)

            access_token_expiration = datetime.now(timezone.utc) + timedelta(hours=1)
            access_token = jwt.encode(
                {
                    "pk": user.pk,
                    "exp": access_token_expiration,
                },
                JWT_SECRET,
                algorithm="HS256",
            )

            return Response({"access_token": access_token})

        except jwt.ExpiredSignatureError:
            return Response({"error": "Refresh token has expired"}, status=401)
        except jwt.DecodeError:
            return Response({"error": "Invalid refresh token"}, status=401)
