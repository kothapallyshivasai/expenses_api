import csv
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ExpenseSerializer
from django.db import transaction
from .models import CustomUserProfile, Expense, ExpenseShare
from django.db import transaction

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(tokens, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            expense = serializer.save()
            if expense.split_method == 'EQUAL':
                split_equal(expense)
            elif expense.split_method == 'EXACT':
                split_exact(expense, request.data['exact_shares'])
            elif expense.split_method == 'PERCENTAGE':
                serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def split_equal(expense):
    participants = expense.participants.all()
    share_amount = expense.amount / len(participants)
    for user in participants:
        ExpenseShare.objects.create(expense=expense, user=user, amount=share_amount)

def split_exact(expense, exact_shares):
    for user_id, share_amount in exact_shares.items():
        user = CustomUserProfile.objects.get(id=user_id)
        ExpenseShare.objects.create(expense=expense, user=user, amount=share_amount)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_balance_sheet_user_individual(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Payer', 'User', 'Expense Description', 'Amount'])

    for expense in Expense.objects.filter(participants__id=request.user.id):
        for share in expense.shares.filter(user=request.user):
            writer.writerow([expense.id, expense.payer, share.user.username, expense.description, share.amount])

    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_balance_sheet_user(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Payer', 'User', 'Expense Description', 'Amount'])

    for expense in Expense.objects.filter(payer=request.user.id):
        for share in expense.shares.all():
            writer.writerow([expense.id, expense.payer, share.user.username, expense.description, share.amount])

    return response