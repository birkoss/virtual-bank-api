from datetime import datetime

from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions.models import Account, Transaction, TransactionCategory
from transactions.api.serializers import (
    UserSerializer as TranUserSerializer, FamilyMemberSerializer)

from ..models import User, Family, FamilyMember

from .serializers import UserSerializer


class loginAsUser(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        # Verify it's a valid Children from the same family
        user = User.objects.filter(
            pk=request.data['user_id'],
            is_children=True,
            familymember__family__familymember__user=request.user
        ).first()

        if user is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': 'Invalid information'
            }, status=status.HTTP_404_NOT_FOUND)

        token = Token.objects.get(user=user)

        return Response({
            'status': status.HTTP_200_OK,
            'token': token.key,
        }, status=status.HTTP_200_OK)


class loginUser(APIView):
    def post(self, request, format=None):

        user = authenticate(
            request,
            email=request.data['email'],
            password=request.data['password'])
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
                request.data['password'],
                firstname=serializer.data['firstname'],
                lastname=serializer.data['lastname'],
                is_children=False
            )

            token = Token.objects.get(user=user)

            # Create a Family instance
            family = Family(user=user)
            family.save()

            # Create a FamilyMember
            familyMember = FamilyMember(user=user, family=family)
            familyMember.save()

            # Set balance of the current account to 1000 and an initial transaction
            account = Account.objects.filter(user=user).first()
            newBalance = 1000

            transaction = Transaction(
                account_to=account,
                account_from=account,
                amount=newBalance,
                date_validated=datetime.now()
            )
            transaction.save()

            Account.objects.filter(user=user).update(balance=newBalance)

            return Response({
                'status': status.HTTP_200_OK,
                'token': token.key,
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)


class usersDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id, format=None):
        if user_id == str(request.user.id):
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "You cannot delete your own user"
            }, status.HTTP_404_NOT_FOUND)

        # Is this a valid user in our family ?
        user = User.objects.filter(
            familymember__family__familymember__user=request.user, id=user_id
        ).first()

        if user is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid user"
            }, status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({
            "status": status.HTTP_200_OK
        })


class familyMembers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.filter(
            familymember__family__familymember__user=request.user
        ).exclude(pk=request.user.pk).order_by("firstname")

        serializer = FamilyMemberSerializer(instance=users, many=True)

        return Response({
            'users': serializer.data,
            'status': status.HTTP_200_OK,
        })


class users(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        # This is only for Parents
        if request.user.is_children:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "Children can't access this.",
            }, status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.filter(
            familymember__family__familymember__user=request.user
        ).order_by("firstname")
        serializer = TranUserSerializer(instance=users, many=True)

        return Response({
            'users': serializer.data,
            'status': status.HTTP_200_OK,
        })

    def post(self, request, format=None):
        # This is only for Parents
        if request.user.is_children:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "Children can't access this.",
            }, status=status.HTTP_401_UNAUTHORIZED)

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

            # Pick our family
            family = Family.objects.filter(user=request.user).first()

            # Add it as a Family Member
            familyMember = FamilyMember(user=user, family=family)
            familyMember.save()

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)


class account(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        serializer = TranUserSerializer(instance=request.user)

        # Determine if we need to show a wizard
        need_wizard = False

        # @TODO: Create Helpers (also used in users endpoint)
        users = User.objects.filter(
            familymember__family__familymember__user=request.user
        ).first()

        if users is None:
            need_wizard = True
        else:
            # @TODO: Create Helpers (also used in transactions endpoint)
            categories = TransactionCategory.objects.filter(
                user=request.user,
                is_active=True
            ).first()

            if categories is None:
                need_wizard = True

        return Response({
            'account': serializer.data,
            'status': status.HTTP_200_OK,
            'need_wizard': need_wizard
        })
