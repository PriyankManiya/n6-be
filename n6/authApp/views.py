from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class UserRegistrationView(APIView):

    def get(self, request, formate=None):
        return Response({'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
