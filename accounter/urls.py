from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('customers/', customers, name='customers'),
    path('suppliers/', suppliers, name='suppliers'),
    path('transactions/', transactions, name='transactions'),
    path('transactions/<str:transaction_type>/', add_transaction, name='add_transaction'),
    path('items/', items, name='items'),
    path('contracts/', create_contract, name='contracts'),
    path('contracts/<int:pk>/', download_file, name='download_file'),
    path('invoice/<int:pk>/', generate_invoice, name='invoice'),
    path('dinvoice/<int:pk>/', download_invoice, name='download_invoice'),
]
