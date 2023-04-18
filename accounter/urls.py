from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('customers/', customers, name='customers'),
    path('suppliers/', suppliers, name='suppliers'),
    path('transactions/', transactions, name='transactions'),
    path('transactions/<str:transaction_type>/', add_transaction, name='add_transaction'),
    path('reports/<str:type>/', some_view, name='reports'),
]
