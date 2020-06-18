from django.urls import path

from . import views as api_views


urlpatterns = [
    path('v1/stats', api_views.stats.as_view(), name='stats'),

    path(
        'v1/transactions',
        api_views.transactions.as_view(),
        name='transactions'
    ),

    path(
        'v1/sendMoney',
        api_views.sendMoney.as_view(),
        name='send-money'
    ),

    path(
        'v1/withdrawMoney',
        api_views.withdrawMoney.as_view(),
        name='withdraw-money'
    ),

    path(
        'v1/transactionsStats',
        api_views.transactionsStats.as_view(),
        name='transactions-stats'
    ),

    path(
        'v1/transactionsCategories',
        api_views.transactionsCategories.as_view(),
        name='transactions-categories'
    ),
    path(
        'v1/transactionsCategories/<str:category_id>',
        api_views.transactionsCategoriesDetails.as_view(),
        name='transactions-categories-details'
    ),

    path(
        'v1/goals',
        api_views.goals.as_view(),
        name='goals'
    ),
    path(
        'v1/goals/<str:goal_id>',
        api_views.goalsDetails.as_view(),
        name='goals-details'
    ),


    path(
        'v1/accounts',
        api_views.accounts.as_view(),
        name='accounts'
    ),
]
