from rest_framework import serializers

from users.api.serializers import UserSerializer

from ..models import Account, AccountType, AccountStatus, TransactionCategory


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


class TransactionCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['id', 'name']
