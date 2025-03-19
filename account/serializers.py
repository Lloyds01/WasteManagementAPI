from rest_framework import serializers
from .models import Transaction, TransactionType 

class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'user_email', 'amount', 'transaction_ref', 'transaction_status',
            'disbursement_source', 'beneficiary_account_number', 'beneficiary_bank_code',
            'beneficiary_bank_name', 'beneficiary_account_name', 'balance_before',
            'balance_after', 'source_account_name', 'source_account_number',
            'source_bank_code', 'transaction_type', 'narration', 'attempt_payout',
            'is_disbursed', 'escrow_id', 'metadata', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_email', 'transaction_ref', 'balance_before', 'balance_after',
            'created_at', 'updated_at', 'transaction_status'
        ]

    def validate_amount(self, value):
        """
        Check that the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value

    def validate_transaction_type(self, value):
        """
        Check that the transaction type is valid.
        """
        if value and value not in dict(TransactionType.choices).keys():  
            valid_types = dict(TransactionType.choices).keys()
            raise serializers.ValidationError(f"Invalid transaction type. Must be one of: {', '.join(valid_types)}")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new Transaction instance, given the validated data.
        """
        # Ensure metadata is a dictionary, not None
        if 'metadata' not in validated_data or validated_data['metadata'] is None:
            validated_data['metadata'] = {}
        
        
        return Transaction.objects.create(**validated_data)