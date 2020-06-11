from django.db import models

from core.models import TimeStampedModel
from users.models import User


class AccountStatus(models.Model):
    name = models.CharField(max_length=100)


class AccountType(models.Model):
    name = models.CharField(max_length=100)


class Account(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    status = models.ForeignKey(AccountStatus, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)


class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)


class Transaction(TimeStampedModel, models.Model):
    account_from = models.ForeignKey(
        Account, related_name="account_from", on_delete=models.CASCADE)
    account_to = models.ForeignKey(
        Account, related_name="account_to", on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date_validated = models.DateTimeField(null=True)
    description = models.CharField(max_length=200, blank=True)
