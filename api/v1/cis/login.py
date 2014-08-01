from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = authenticate(**{k: v[0] for k, v in dict(request.DATA).items() if len(v)})
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('api-v1-login'))
