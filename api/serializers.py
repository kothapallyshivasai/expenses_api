from decimal import Decimal
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUserProfile, Expense, ExpenseShare

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUserProfile
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('is_superuser', None)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ExpenseShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseShare
        fields = ['id', 'expense', 'user', 'amount']

class ExpenseSerializer(serializers.ModelSerializer):
    shares = ExpenseShareSerializer(many=True, read_only=True)
    percentage_shares = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = Expense
        fields = ['id', 'payer', 'participants', 'amount', 'description', 'split_method', 'created_at', 'shares', 'percentage_shares']

    def validate(self, data):
        if data['split_method'] == 'PERCENTAGE':
            percentage_shares = self.initial_data.get('percentage_shares', {})
            percentages = percentage_shares.values()
            if sum(percentages) != 100:
                raise serializers.ValidationError("Percentages must add up to 100%.")
        return data

    def create(self, validated_data):
        percentage_shares = validated_data.pop('percentage_shares', None)
        expense = super().create(validated_data)
        if expense.split_method == 'PERCENTAGE' and percentage_shares:
            for user_id, percentage in percentage_shares.items():
                user = CustomUserProfile.objects.get(id=user_id)
                share_amount = (Decimal(percentage) / Decimal(100)) * expense.amount
                ExpenseShare.objects.create(expense=expense, user=user, amount=share_amount)
        return expense