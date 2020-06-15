from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.registerUser.as_view(), name='register'),
    path('api/login', api_views.loginUser.as_view(), name='login'),

    path('api/account', api_views.account.as_view(), name='account'),

    path('api/users', api_views.users.as_view(), name='users'),
    path('api/users/<str:user_id>',
         api_views.usersDetails.as_view(), name='users-details'),
]
