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
        'v1/accounts',
        api_views.accounts.as_view(),
        name='accounts'
    ),
]
