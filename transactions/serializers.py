# from rest_framework import serializers
# from .models import Transaction

# class TransactionSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')

#     class Meta:
#         model = Transaction
#         fields = ['id', 'user', 'amount', 'type', 'description', 'metadata', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'created_at', 'updated_at']

#     def create(self, validated_data):
#         """
#         Create and return a new Transaction instance, given the validated data.
#         """
#         # Ensure metadata is a dictionary, not None
#         if 'metadata' not in validated_data or validated_data['metadata'] is None:
#             validated_data['metadata'] = {}
        
#         return Transaction.objects.create(**validated_data)

#     def validate_amount(self, value):
#         """
#         Check that the amount is positive.
#         """
#         if value <= 0:
#             raise serializers.ValidationError("Amount must be positive.")
#         return value

#     def validate_type(self, value):
#         """
#         Check that the transaction type is valid.
#         """
#         valid_types = dict(Transaction.TRANSACTION_TYPES).keys()
#         if value not in valid_types:
#             raise serializers.ValidationError(f"Invalid transaction type. Must be one of: {', '.join(valid_types)}")
#         return value