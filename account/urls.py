# account/urls.py
from django.urls import path
from .views import TransactionListCreateView, TransactionHistoryView

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/history/', TransactionHistoryView.as_view(), name='transaction-history'),
]