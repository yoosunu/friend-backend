from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from config.settings import JWT_SECRET
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        if not token:
            return None

        try:
            decoded = jwt.decode(
                token,
                JWT_SECRET,
                algorithms="HS256",
            )
        except ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("invaild token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            return AuthenticationFailed("user not found")
