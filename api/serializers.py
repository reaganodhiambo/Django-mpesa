from rest_framework import serializers
from .models import Transation, ResponseBody
from .validators import validate_phone_number
from django.core.validators import MinValueValidator
from .utils import stk_push


class StkPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)
    amount = serializers.IntegerField(validators=[MinValueValidator(1)])

    def create(self, validated_data):
        phonenumber = validated_data["phone_number"]
        amount = validated_data["amount"]

        if str(phonenumber)[0] == "+":
            phonenumber = phonenumber[1:]
        elif str(phonenumber)[0] == "0":
            phonenumber = "254" + phonenumber[1:]

        payment = stk_push(amount=amount, phonenumber=phonenumber)

        return payment


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transation
        fields = "__all__"


class ResponseBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseBody
        fields = "__all__"

    def create(self, validated_data):
        return ResponseBody.objects.create(**validated_data)
