from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUserProfile, Expense, ExpenseShare
from django.urls import reverse
from decimal import Decimal

class ExpenseAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()        
        self.user = CustomUserProfile.objects.create_user(username='testuser', password='password')
        CustomUserProfile.objects.create_user(username='testuser2', password='password')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_add_expense(self):
        url = reverse('add-expense')  
        
        data = {
            "payer": self.user.id,
            "participants": [self.user.id, 2],
            "amount": "2000.00",
            "description": "Dinner",
            "split_method": "EQUAL",
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(ExpenseShare.objects.count(), 2)

    def test_download_balance_sheet_user_individual(self):
        url = reverse('download_balance_sheet_user_individual')
        response = self.client.get(url, format='csv')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue(response.content.startswith(b'ID,Payer,User,Expense Description,Amount'))

    def test_download_balance_sheet_user(self):
        url = reverse('download_balance_sheet_user')
        response = self.client.get(url, format='csv')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue(response.content.startswith(b'ID,Payer,User,Expense Description,Amount'))

class ExpenseModelTests(TestCase):
    def setUp(self):
        self.payer = CustomUserProfile.objects.create_user(username='payer', password='password')
        self.participant1 = CustomUserProfile.objects.create_user(username='participant1', password='password')
        self.participant2 = CustomUserProfile.objects.create_user(username='participant2', password='password')

    def test_expense_split_equal(self):
        expense = Expense.objects.create(
            payer=self.payer,
            amount=Decimal('2000.00'),
            description="Dinner",
            split_method='EQUAL'
        )
        expense.participants.set([self.participant1.id, self.participant2.id])
        expense.save()
        share_amount = expense.amount / expense.participants.count()
        for participant in expense.participants.all():
            ExpenseShare.objects.create(expense=expense, user=participant, amount=share_amount)
        
        shares = ExpenseShare.objects.filter(expense=expense)
        self.assertEqual(shares.count(), 2)
        self.assertEqual(shares.filter(user=self.participant1).first().amount, Decimal('1000.00'))
        self.assertEqual(shares.filter(user=self.participant2).first().amount, Decimal('1000.00'))

    def test_expense_split_percentage(self):
        expense = Expense.objects.create(
            payer=self.payer,
            amount=Decimal('2000.00'),
            description="Party",
            split_method='PERCENTAGE'
        )
        expense.participants.set([self.participant1.id, self.participant2.id])
        expense.save()
        
        percentage_shares = {
            self.participant1.id: 50,
            self.participant2.id: 50,
        }
        
        for user_id, percentage in percentage_shares.items():
            user = CustomUserProfile.objects.get(id=user_id)
            share_amount = (Decimal(percentage) / Decimal('100')) * expense.amount
            ExpenseShare.objects.create(expense=expense, user=user, amount=share_amount)
        
        shares = ExpenseShare.objects.filter(expense=expense)
        self.assertEqual(shares.count(), 2)
        self.assertEqual(shares.filter(user=self.participant1).first().amount, Decimal('1000.00'))
        self.assertEqual(shares.filter(user=self.participant2).first().amount, Decimal('1000.00'))