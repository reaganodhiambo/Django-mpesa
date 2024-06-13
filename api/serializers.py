from rest_framework import serializers
from .models import Transation, ResponseBody
from .validators import validate_phone_number


class StkPushSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transation
        fields = "__all__"


class ResponseBodySerializer(serializers.Serializer):
    class Meta:
        model = ResponseBody
        fields = "__all__"

    def create(self, validated_data):
        return ResponseBody.objects.create(**validated_data)
