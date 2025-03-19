# account/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Transaction
import uuid

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
            amount=100.00,
            transaction_type='deposit',
            narration='Test deposit',
            metadata={}
        )
    
    def test_transaction_creation(self):
        """Test that a transaction can be created"""
        self.assertEqual(self.transaction.amount, 100.00)
        self.assertEqual(self.transaction.transaction_type, 'deposit')
        self.assertEqual(self.transaction.narration, 'Test deposit')
        self.assertEqual(self.transaction.user, self.user)
    
    def test_transaction_str_representation(self):
        """Test the string representation of a transaction"""
        expected_str = f"{self.transaction.transaction_ref} - {self.transaction.amount} by {self.user.email}"
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
            'amount': 200.00,
            'transaction_type': 'deposit',
            'narration': 'API test deposit'
        }
        
        self.url = reverse('transaction-list-create')
        self.history_url = reverse('transaction-history')
        
        # Create some test transactions
        Transaction.objects.create(
            user=self.user,
            amount=100.00,
            transaction_type='deposit',
            narration='First deposit',
            metadata={}
        )
        
        Transaction.objects.create(
            user=self.user,
            amount=50.00,
            transaction_type='withdrawal',
            narration='First withdrawal',
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
        self.assertEqual(Transaction.objects.latest('created_at').amount, 200.00)
    
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
        response = self.client.get(f"{self.url}?transaction_type=deposit")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['transaction_type'], 'deposit')
    
    def test_transaction_success_message(self):
        """Test that the API returns the correct success message"""
        response = self.client.post(
            self.url,
            self.transaction_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Deposit transaction initiated successfully')
        
    def test_negative_amount_validation(self):
        """Test that negative amounts are rejected"""
        invalid_data = {
            'amount': -50.00,
            'transaction_type': 'deposit',
            'narration': 'Invalid deposit'
        }
        
        response = self.client.post(
            self.url,
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)

def test_unauthenticated_access(self):
    """Test that unauthenticated requests are rejected"""
    # Create a new client without authentication
    client = APIClient()
    
    response = client.get(self.url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    response = client.post(
        self.url,
        self.transaction_data,
        format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_pagination(self):
    """Test that pagination works correctly"""
    # Create more transactions to test pagination
    for i in range(15):  # Create 15 more transactions
        Transaction.objects.create(
            user=self.user,
            amount=10.00 * i,
            transaction_type='deposit',
            narration=f'Pagination test {i}',
            metadata={}
        )
    
    response = self.client.get(self.url)
    
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 10)  # Default page size
    self.assertIsNotNone(response.data['next'])  # Should have a next page
    
    # Test second page
    response = self.client.get(response.data['next'])
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data['results']), 7)  # 17 total items, 7 on second page