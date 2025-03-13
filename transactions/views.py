# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from .models import Transaction
# from .serializers import TransactionSerializer
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
# from django.contrib.auth import get_user_model

# from rest_framework.pagination import PageNumberPagination

# User = get_user_model()

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class TransactionListCreateView(generics.ListCreateAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.AllowAny]
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['type', 'created_at']
#     ordering_fields = ['amount', 'created_at']
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         # For testing, return all transactions or a subset
#         return Transaction.objects.all()

#     def perform_create(self, serializer):
#         # For testing, use a default user
#         default_user = User.objects.first()  # Just get the first user
#         if not default_user:
#             # If no users exist, create one
#             default_user = User.objects.create(
#                 email='test@example.com',
#                 first_name='Test',
#                 last_name='User'
#             )
        
#         # Ensure metadata is a dictionary, not None
#         metadata = serializer.validated_data.get('metadata', {})
#         if metadata is None:
#             metadata = {}
        
#         serializer.save(user=default_user, metadata=metadata)
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
        
#         # Get the transaction type and create a custom success message
#         transaction_type = serializer.data.get('type', '')
#         success_message = f"{transaction_type.capitalize()} successful"
        
#         # Return a custom response with the success message
#         response_data = {
#             'status': 'success',
#             'message': success_message,
#             'data': serializer.data
#         }
        
#         return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

# class TransactionHistoryView(generics.ListAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.AllowAny]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filterset_fields = ['type', 'created_at']
#     ordering_fields = ['amount', 'created_at']

#     def get_queryset(self):
#         # For testing, return all transactions or a subset
#         return Transaction.objects.all()