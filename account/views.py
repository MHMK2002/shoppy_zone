from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User


class SignUpView(APIView):

    def post(self, request: Request):
        username = request.data.get('username')
        if not username:
            return Response(data={'username': 'you must provide this field'}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if not password:
            return Response(data={'password': 'you must provide this field'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        if not email:
            return Response(data={'email': 'you must provide this field'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response(data={'message': 'You are successfully signup.'}, status=status.HTTP_201_CREATED)
