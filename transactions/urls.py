from django.urls import path
from .views import TransactionListCreateView, TransactionHistoryView

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('history/', TransactionHistoryView.as_view(), name='transaction-history'),
]