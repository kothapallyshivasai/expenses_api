from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserProfile(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Expense(models.Model):
    
    SPLIT_METHODS = [
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage')
    ]

    payer = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE, related_name='expenses_paid')
    participants = models.ManyToManyField(CustomUserProfile, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHODS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer} - {self.amount} ({self.split_method})"
    

class ExpenseShare(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} owes {self.amount} for {self.expense.description}"