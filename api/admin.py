from django.contrib import admin

from .models import CustomUserProfile, Expense, ExpenseShare

# Register your models here.
admin.site.register(CustomUserProfile)
admin.site.register(Expense)
admin.site.register(ExpenseShare)