from datetime import datetime

from django.db.models import Count, Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Family

from ..models import Account, TransactionCategory, Transaction

from .serializers import (AccountSerializer, TransactionSerializer,
                          TransactionWriteSerializer,
                          TransactionCategorySerializer,
                          TransactionCategoryWriteSerializer)


class transactions(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        filters = Q()
        filters.add(Q(account_to__user=request.user), Q.OR)
        filters.add(Q(account_from__user=request.user), Q.OR)

        transactions = Transaction.objects.filter(
            filters
        ).order_by("-date_added")[:30]

        serializer = TransactionSerializer(
            instance=transactions, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'transactions': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = TransactionWriteSerializer(data=request.data)

        account = Account.objects.filter(user=request.user).first()

        if serializer.is_valid():
            # Watch the balance first
            if account.balance < int(request.data['amount']):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    'message': "Not enough balance to do this",
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(account_from=account,
                            date_validated=datetime.now())

            amount = serializer.data['amount']

            # Reduce the balance of the sender
            account.balance -= amount
            account.save()

            # Increate the receiver balance
            account2 = Account.objects.filter(
                pk=serializer.data['account_to']).first()
            account2.balance += amount
            account2.save()

            return Response({
                'balance': account.balance,
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


class transactionsStats(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = TransactionCategory.objects.filter(
            user__family__familymember__user=request.user,
            transaction__account_to__user=request.user
        ).annotate(transactions=Count('transaction')).order_by("name")

        serializer = TransactionCategorySerializer(
            instance=categories, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'transactionsCategories': serializer.data
        }, status=status.HTTP_200_OK)
