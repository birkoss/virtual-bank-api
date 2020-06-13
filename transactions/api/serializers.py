from rest_framework import serializers

from users.api.serializers import UserSerializer

from users.models import User

from ..models import Account, AccountType, AccountStatus, Transaction, TransactionCategory


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatus
        fields = ['id', 'name']


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name']


class AccountSerializer(serializers.ModelSerializer):
    type = AccountTypeSerializer(read_only=True)
    status = AccountStatusSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'balance', 'type', 'status', 'user']


class TransactionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'description', 'account_to']


class TransactionCategorySerializer(serializers.ModelSerializer):
    transactions = serializers.IntegerField()

    class Meta:
        model = TransactionCategory
        fields = ['id', 'name', 'transactions']


class TransactionCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name']
