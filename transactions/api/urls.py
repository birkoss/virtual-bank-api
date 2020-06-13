from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/stats', api_views.stats.as_view(), name='stats'),

    path('api/transactions', api_views.transactions.as_view(),
         name='transactions'),


    path('api/transactionsCategories', api_views.transactionsCategories.as_view(),
         name='transactions-categories'),
    path('api/transactionsCategories/<str:category_id>', api_views.transactionsCategoriesDetails.as_view(),
         name='transactions-categories-details'),
]
