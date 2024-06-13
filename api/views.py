from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import stk_push
from .models import Transation, ResponseBody
from .serializers import StkPushSerializer, ResponseBodySerializer

# Create your views here.


class StkPushView(APIView):
    queryset = Transation.objects.all()
    serializer_class = StkPushSerializer

    def get(self,request):
        serializer = StkPushSerializer()
        return Response(status=status.HTTP_200_OK)

        return response.Response({"transactions": serializer.data})
    def post(self, request):
        serializer = StkPushSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            amount = str(data["amount"])
            phonenumber = data["phone_number"]

            # call stk_push from utils
            try:
                response = stk_push(amount=amount, phonenumber=phonenumber)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CallbackView(APIView):
    """
    View to handle Mpesa callback data and transaction management.
    """
    def get(self, request):
        transactions = Transation.objects.all()
        serializer = StkPushSerializer(transactions,many=True)
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ResponseBodySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            mpesa_data = serializer.validated_data["body"]

            if mpesa_data['stkCallback']['ResultCode'] == 0:
                print("success")
                transaction = Transation.objects.create(
                    phonenumber=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
                    amount=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
                    receipt_no=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"]
                )
                return Response(
                    {"message": "Callback Data received and processed successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                # Handle unsuccessful transaction (log error or notify)
                print(
                    f"Mpesa Callback Error: {mpesa_data['stkCallback']['ResultDesc']}"
                )
                return Response(
                    {"error": "Mpesa Callback processing failed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
