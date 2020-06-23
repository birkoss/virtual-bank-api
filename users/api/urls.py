from django.urls import path

from . import views as api_views


urlpatterns = [
    path('v1/register', api_views.registerUser.as_view(), name='register'),
    path('v1/login', api_views.loginUser.as_view(), name='login'),

    path('v1/loginAs', api_views.loginAsUser.as_view(), name='login-as'),

    path('v1/account', api_views.account.as_view(), name='account'),

    path('v1/familyMembers', api_views.familyMembers.as_view(),
         name='family-members'),

    path('v1/users', api_views.users.as_view(), name='users'),
    path('v1/users/<str:user_id>',
         api_views.usersDetails.as_view(), name='users-details'),
]
