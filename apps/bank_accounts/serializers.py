from rest_framework import serializers
from .models import BankAccount, Transaction


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            "id",
            "institution_name",
            "institution_id",
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "account_id",
            "name",
            "amount",
            "date",
            "payment_channel",
            "pending",
            "category",
            "payment_channel",
            "image",
        ]
