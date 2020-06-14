from rest_framework import serializers

from users.models import User

from ..models import (Account, AccountType, AccountStatus,
                      Transaction, TransactionCategory)


class AccountStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountStatus
        fields = ['id', 'name']


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name']


class AccountPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id']


class AccountSerializer(serializers.ModelSerializer):
    type = AccountTypeSerializer(read_only=True)
    status = AccountStatusSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'balance', 'type', 'status']


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


class UserSerializer(serializers.ModelSerializer):
    accounts = AccountPreviewSerializer(source='account_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname',
                  'lastname', 'is_children', 'accounts']
