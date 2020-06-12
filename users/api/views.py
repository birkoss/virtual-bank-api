from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User, Family

from .serializers import UserSerializer


class loginUser(APIView):
    def post(self, request, format=None):

        user = authenticate(
            request, email=request.data['email'], password=request.data['password'])
        if user is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': 'Invalid information'
            }, status=status.HTTP_404_NOT_FOUND)

        login(request, user)

        token = Token.objects.get(user=user)

        return Response({
            'status': status.HTTP_200_OK,
            'token': token.key,
        }, status=status.HTTP_200_OK)


class registerUser(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.data['email'],
                request.data['password']
            )

            token = Token.objects.get(user=user)

            return Response({
                'status': status.HTTP_200_OK,
                'token': token.key,
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)


class users(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.filter(
            families__master=request.user).order_by("firstname")
        serializer = UserSerializer(instance=users, many=True)

        return Response({
            'users': serializer.data,
            'status': status.HTTP_200_OK,
        })

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            # Add the new user
            user = User.objects.create_user(
                serializer.data['email'],
                request.data['password'],
                firstname=request.data['firstname'],
                lastname=request.data['lastname'],
                is_children=request.data['isChildren']
            )

            # Add it to our family
            current_user = User.objects.get(pk=request.user.id)
            family = Family(slave=user, master=current_user)
            family.save()

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)
