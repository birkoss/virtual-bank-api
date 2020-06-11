from django.contrib import admin
from django.urls import path

from users.api.urls import urlpatterns as users_urlpatterns
from transactions.api.urls import urlpatterns as transactions_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
] + users_urlpatterns + transactions_urlpatterns
