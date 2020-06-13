from django.db import models

from core.models import TimeStampedModel, UUIDModel
from users.models import User


class AccountStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AccountType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(UUIDModel, TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    status = models.ForeignKey(AccountStatus, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.email + " - " + str(self.id)


class TransactionCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(UUIDModel, TimeStampedModel, models.Model):
    account_from = models.ForeignKey(
        Account, related_name="account_from", on_delete=models.CASCADE)
    account_to = models.ForeignKey(
        Account, related_name="account_to", on_delete=models.CASCADE)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date_validated = models.DateTimeField(null=True)
    description = models.CharField(max_length=200, blank=True)
