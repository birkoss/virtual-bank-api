from django.contrib import admin

from .models import User, Family, FamilyMember

admin.site.register(User)
admin.site.register(Family)
admin.site.register(FamilyMember)
