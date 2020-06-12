from django.contrib import admin

from .models import User, Family

admin.site.register(User)
admin.site.register(Family)
