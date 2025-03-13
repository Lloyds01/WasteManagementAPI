from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Transaction
from decimal import Decimal
import json

User = get_user_model()

class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        self.transaction = Transaction.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            type='deposit',
            description='Test deposit',
            metadata={}
        )
    
    def test_transaction_creation(self):
        """Test that a transaction can be created"""
        self.assertEqual(self.transaction.amount, Decimal('100.00'))
        self.assertEqual(self.transaction.type, 'deposit')
        self.assertEqual(self.transaction.description, 'Test deposit')
        self.assertEqual(self.transaction.user, self.user)
    
    def test_transaction_str_representation(self):
        """Test the string representation of a transaction"""
        expected_str = f"deposit - 100.00 by {self.user.email}"
        self.assertEqual(str(self.transaction), expected_str)

class TransactionAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        
        self.transaction_data = {
            'amount': '200.00',
            'type': 'deposit',
            'description': 'API test deposit'
        }
        
        self.url = reverse('transaction-list-create')
        self.history_url = reverse('transaction-history')
        
        # Create some test transactions
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            type='deposit',
            description='First deposit',
            metadata={}
        )
        
        Transaction.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            type='withdrawal',
            description='First withdrawal',
            metadata={}
        )
    
    def test_create_transaction(self):
        """Test creating a transaction via the API"""
        response = self.client.post(
            self.url,
            self.transaction_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 3)
        self.assertEqual(Transaction.objects.latest('created_at').amount, Decimal('200.00'))
    
    def test_list_transactions(self):
        """Test listing transactions via the API"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming pagination is enabled
    
    def test_transaction_history(self):
        """Test the transaction history endpoint"""
        response = self.client.get(self.history_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming pagination is enabled
    
    def test_filter_transactions_by_type(self):
        """Test filtering transactions by type"""
        response = self.client.get(f"{self.url}?type=deposit")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['type'], 'deposit')
    
    def test_order_transactions_by_amount(self):
        """Test ordering transactions by amount"""
        response = self.client.get(f"{self.url}?ordering=-amount")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['amount'], '100.00')
        self.assertEqual(response.data['results'][1]['amount'], '50.00')
    
    def test_validate_amount(self):
        """Test validation for negative amount"""
        invalid_data = self.transaction_data.copy()
        invalid_data['amount'] = '-50.00'
        
        response = self.client.post(
            self.url,
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)
    
    def test_validate_type(self):
        """Test validation for invalid transaction type"""
        invalid_data = self.transaction_data.copy()
        invalid_data['type'] = 'invalid_type'
        
        response = self.client.post(
            self.url,
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('type', response.data)
        
        
        
        
    def test_transaction_success_message(self):
        """Test that the API returns the correct success message"""
        response = self.client.post(
            self.url,
            self.transaction_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Deposit successful')
        
        # Test with a different transaction type
        withdrawal_data = self.transaction_data.copy()
        withdrawal_data['type'] = 'withdrawal'
        
        response = self.client.post(
            self.url,
            withdrawal_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Withdrawal successful')

# Create your tests here.
def test_addition():
    assert 1 + 1 == 2
