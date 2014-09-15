from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from zonesapp.serializers import UserSerializer

from django.contrib.auth import logout, login




from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})



@api_view(['POST'])
def create_auth(request):

    data = JSONParser().parse(request)
    serialized = UserSerializer(data=data)
    model = User
    if serialized.is_valid():
        user = User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        user.save()
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data, status=status.HTTP_201_CREATED, headers={"Access-Control-Allow-Origin": "http://127.0.0.1:8000/"})
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin": "http://127.0.0.1:8000/"})




