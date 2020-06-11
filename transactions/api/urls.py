from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/stats', api_views.stats.as_view(), name='stats'),
]
