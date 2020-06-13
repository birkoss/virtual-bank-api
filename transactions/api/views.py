from datetime import datetime

from django.db.models import Count, Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from ..models import Account, TransactionCategory

from .serializers import (AccountSerializer, TransactionWriteSerializer,
                          TransactionCategorySerializer,
                          TransactionCategoryWriteSerializer)


class transactions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = TransactionCategory.objects.filter(
            user=request.user
        ).annotate(transactions=Count('transaction')).order_by("name")
        serializer = TransactionCategorySerializer(
            instance=categories, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'transactionsCategories': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TransactionWriteSerializer(data=request.data)

        account = Account.objects.filter(user=request.user).first()

        if serializer.is_valid():
            serializer.save(account_from=account,
                            date_validated=datetime.now())

            # Reduce the balance and increase the other balance

            return Response({
                'balance': 100,  # @TODO: Return the correct balance
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class transactionsCategoriesDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, category_id, format=None):
        category = TransactionCategory.objects.filter(
            id=category_id, user=request.user).first()
        if category is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid category"
            }, status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({
            "status": status.HTTP_200_OK
        })


class transactionsCategories(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = TransactionCategory.objects.filter(
            user=request.user
        ).annotate(transactions=Count('transaction')).order_by("name")
        serializer = TransactionCategorySerializer(
            instance=categories, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'transactionsCategories': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TransactionCategoryWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class stats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        accounts = Account.objects.filter(user=request.user)

        serializer = AccountSerializer(instance=accounts, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'accounts': serializer.data,
        })


class accounts(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.filter(pk=request.user.pk).first()
        print(user.friends)
        print(request.user.friends)
        filters = Q()
        filters.add(Q(user__families__slave=request.user), Q.OR)
        filters.add(Q(user__friends__slave=request.user), Q.OR)

        accounts = Account.objects.filter(
            filters
        ).order_by("user__firstname")

        serializer = AccountSerializer(
            instance=accounts, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'accounts': serializer.data
        }, status=status.HTTP_200_OK)
