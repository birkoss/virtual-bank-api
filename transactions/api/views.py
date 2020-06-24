from datetime import datetime

from django.db.models import Count, Q

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Family

from ..models import Account, TransactionCategory, Transaction, Goal

from .serializers import (AccountSerializer, TransactionSerializer,
                          TransactionWriteSerializer,
                          TransactionCategorySerializer,
                          TransactionCategoryWriteSerializer, GoalSerializer)

from core.helpers import send_push_message


def createTransaction(serializer, accountFrom, accountTo, amount):
    serializer.save(account_from=accountFrom, date_validated=datetime.now())

    accountFrom.balance -= amount
    accountFrom.save()

    accountTo.balance += amount
    accountTo.save()


class sendMoney(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = TransactionWriteSerializer(data=request.data)

        accountFrom = Account.objects.filter(user=request.user).first()

        if serializer.is_valid():
            # Watch the balance first
            if accountFrom.balance < int(request.data['amount']):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    'message': "Not enough balance to do this",
                }, status=status.HTTP_400_BAD_REQUEST)

            amount = serializer.validated_data['amount']

            accountTo = serializer.validated_data['account_to']

            createTransaction(serializer, accountFrom, accountTo, amount)

            # Notify the recipient
            user_to = User.objects.filter(account=accountTo).first()

            if user_to is not None and user_to.expo_token != "" and user_to.expo_token is not None:
                send_push_message(user_to.expo_token, request.user.firstname +
                                  " sent you " + str(amount) + " $")

            return Response({
                'balance': accountFrom.balance,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


class withdrawMoney(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        # This is only for Parents
        if request.user.is_children:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "Children can't access this.",
            }, status=status.HTTP_401_UNAUTHORIZED)

        accountTo = Account.objects.filter(user=request.user).first()

        accountFrom = Account.objects.filter(
            pk=request.data['account_to'],
            user__familymember__family__familymember__user=request.user
        ).first()

        if accountFrom is None:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "You can't withdraw outside your family",
            }, status=status.HTTP_401_UNAUTHORIZED)

        request.data['account_to'] = accountTo.pk
        serializer = TransactionWriteSerializer(data=request.data)

        if serializer.is_valid():

            amount = serializer.validated_data['amount']

            createTransaction(serializer, accountFrom, accountTo, amount)

            # Notify the recipient
            user_from = User.objects.filter(account=accountFrom).first()

            if user_from is not None and user_from.expo_token != "" and user_to.expo_token is not None:
                send_push_message(user_from.expo_token, request.user.firstname +
                                  " withdraw " + str(amount) + " $ from your account")

            return Response({
                'balance': accountTo.balance,
                'status': status.HTTP_200_OK,
            })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


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

    # @TODO : REMOVE once the app is accepted on Apple and Android
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
            id=category_id, user=request.user
        ).annotate(transactions=Count('transaction')).first()

        if category is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid category"
            }, status.HTTP_404_NOT_FOUND)

        if category.transactions == 0:
            category.delete()
        else:
            category.is_active = False
            category.save()

        return Response({
            "status": status.HTTP_200_OK
        })


class transactionsCategories(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = TransactionCategory.objects.filter(
            user__family__familymember__user=request.user,
            is_active=True
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


class goalsDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, goal_id, format=None):
        goal = Goal.objects.filter(
            id=goal_id, account__user=request.user
        ).first()

        if goal is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not a valid goal"
            }, status.HTTP_404_NOT_FOUND)

        goal.delete()

        return Response({
            "status": status.HTTP_200_OK
        })


class goals(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        account = Account.objects.filter(user=request.user).first()

        goals = Goal.objects.filter(account=account)

        serializer = GoalSerializer(instance=goals, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'goals': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = GoalSerializer(data=request.data)

        account = Account.objects.filter(user=request.user).first()

        if serializer.is_valid():
            serializer.save(account=account)

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
        accounts_serializer = AccountSerializer(instance=accounts, many=True)

        goals = Goal.objects.filter(account__user=request.user)
        goals_serializer = GoalSerializer(instance=goals, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'accounts': accounts_serializer.data,
            'goals': goals_serializer.data,
        })


class accounts(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.filter(pk=request.user.pk).first()

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
