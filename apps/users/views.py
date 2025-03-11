import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)


def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str] = None) -> None:

    cookie_settings = {
        "path": settings.AUTH_COOKIE_PATH,
        "secure": settings.AUTH_COOKIE_SECURE,
        "httponly": settings.AUTH_COOKIE_HTTPONLY,
        "samesite": settings.AUTH_COOKIE_SAMESITE,
        "max_age": settings.AUTH_COOKIE_ACCESS_MAX_AGE,
    }
    response.set_cookie("access", access_token, **cookie_settings)

    response.set_cookie("access", access_token, **cookie_settings)
    if refresh_token:
        refresh_token_lifetine = settings.AUTH_COOKIE_REFRESH_MAX_AGE
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetine
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_res = super().post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(token_res, access_token=access_token, refresh_token=refresh_token)
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                token_res.data["message"] = "Login Successful."
            else:
                token_res.data["message"] = "Login Failed"
                logger.error(
                    "Access or refresh token not found in login response data.")

        return token_res


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(
                    response,
                    access_token=access_token,
                    refresh_token=refresh_token
                )
                response.data.pop("access", None)
                response.data.pop("refresh", None)
                response.data["message"] = "Access tokens refreshed successfully."
            else:
                response.data["message"] = "Access or refresh tokens not found in refresh response data."
                logger.error(
                    "Access or refresh token not found in resfresh response data.")
        return response


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(response, access_token=access_token, refresh_token=refresh_token)
                response.data.pop("access", None)
                response.data.pop("refresh", None)
                response.data["message"] = "You are logged in Successful."
            else:
                response.data["message"] = "Access or refresh not found in provider response."
                logger.error(
                    "Access or refresh token not found in provider response data.")
        return response


class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
