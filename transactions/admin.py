from django.contrib import admin

from .models import Transaction, TransactionCategory, AccountStatus, AccountType, Account

admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(TransactionCategory)
admin.site.register(AccountStatus)
admin.site.register(AccountType)
