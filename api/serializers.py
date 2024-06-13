from rest_framework import serializers
from .models import Transation
from .validators import validate_phone_number


class StkPushSerializer(serializers.ModelSerializer):
    # phone_number = serializers.CharField(max_length=44)
    # amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    # # account_reference = serializers.CharField(max_length=50)
    # # transaction_description = serializers.CharField(max_length=100)

    class Meta:
        model = Transation
        fields = [
            "phone_number",
            "amount",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
