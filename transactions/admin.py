from django.contrib import admin

from .models import (Transaction, TransactionCategory,
                     AccountStatus, AccountType, Account, Goal)

admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Goal)
admin.site.register(TransactionCategory)
admin.site.register(AccountStatus)
admin.site.register(AccountType)
