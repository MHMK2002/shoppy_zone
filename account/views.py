from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from account.serializers import SignUpSerializer, ProfileSerializer


class SignUpView(APIView):

    def post(self, request: Request):
        serializer = SignUpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors})

        User.objects.create_user(**serializer.validated_data)
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request: Request):
        user = request.user
        serializer = ProfileSerializer(instance=user)
        return Response(data=serializer.data)

    def put(self, request: Request):
        user = request.user
        serializer = ProfileSerializer(instance=user, data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors})
        serializer.save()
        return Response(data=serializer.data)
