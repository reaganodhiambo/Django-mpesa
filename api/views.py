from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StkPushSerializer
from .models import Transation
from .utils import stk_push

# Create your views here.


class StkPushView(APIView):
    queryset = Transation.objects.all()
    serializer_class = StkPushSerializer

    def post(self, request):
        serializer = StkPushSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            amount = data["amount"]
            phonenumber = data["phone_number"]

            # call stk_push from utils
            try:
                response = stk_push(amount, phonenumber)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallbackView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # handle callback from mpesa
        data = request.body
        return gateway.callback(json.loads(data))
