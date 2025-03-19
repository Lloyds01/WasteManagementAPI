from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Transaction, TransactionStatus
from .serializers import TransactionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    # Change to IsAuthenticated
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_status', 'transaction_type', 'created_at']
    ordering_fields = ['amount', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Filter transactions to only show those belonging to the authenticated user
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Use the authenticated user from the request
        user = self.request.user
        
        # Ensure metadata is a dictionary, not None
        metadata = serializer.validated_data.get('metadata', {})
        if metadata is None:
            metadata = {}
        
        # Calculate balance before and after
        # In a real app, you might want to get the actual balance from the user's account
        balance_before = 1000.00  # Example value or user.account.balance if available
        amount = serializer.validated_data.get('amount', 0)
        transaction_type = serializer.validated_data.get('transaction_type')
        
        if transaction_type in ['withdrawal', 'payment']:
            balance_after = balance_before - amount
        else:  # deposit, transfer, refund
            balance_after = balance_before + amount
        
        serializer.save(
            user=user,  # Use the authenticated user
            metadata=metadata,
            balance_before=balance_before,
            balance_after=balance_after,
            transaction_status=TransactionStatus.PENDING
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Get the transaction type and create a custom success message
        transaction_type = serializer.data.get('transaction_type', '')
        if transaction_type:
            success_message = f"{transaction_type.capitalize()} transaction initiated successfully"
        else:
            success_message = "Transaction initiated successfully"
        
        # Return a custom response with the success message
        response_data = {
            'status': 'success',
            'message': success_message,
            'data': serializer.data
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    # Change to IsAuthenticated
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_status', 'transaction_type', 'created_at']
    ordering_fields = ['amount', 'created_at']

    def get_queryset(self):
        # Filter transactions to only show those belonging to the authenticated user
        return Transaction.objects.filter(user=self.request.user)