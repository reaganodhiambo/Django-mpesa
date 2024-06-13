from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import stk_push
from .models import Transation, ResponseBody
from .serializers import TransactionSerializer, ResponseBodySerializer, StkPushSerializer

# Create your views here.
class StkPushView(APIView):
    def post(self,request):
        serializer = StkPushSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(response,status=status.HTTP_201_CREATED,)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallbackView(APIView):
    """
    View to handle Mpesa callback data and transaction management.
    """

    def post(self, request):
        body = request.data
        if body:
            mpesa = ResponseBody.objects.create(body=body)
            print("pass1")
            mpesa_data = mpesa.body
            if mpesa_data['Body']['stkCallback']['ResultCode'] == 0:
                print("pass2")
                transaction = Transation.objects.create(
                    phonenumber=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
                    amount=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
                    receipt_no=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"]
                )
                print("pass3")
            else:
                print("pass4")
            return Response(
                    {"message": "Callback Data received and processed successfully."},
                    status=status.HTTP_201_CREATED,
                )
 
        return Response(
            {"error": "Mpesa Callback processing failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        

    def get(self, request):
        response = ResponseBody.objects.all()
        serializer = ResponseBodySerializer(response,many=True)
        return Response({"responses":serializer.data},status=status.HTTP_200_OK)


# class StkPushView(APIView):
#     queryset = Transation.objects.all()
#     serializer_class = TransactionSerializer

#     def get(self,request):
#         serializer = TransactionSerializer()
#         return Response(status=status.HTTP_200_OK)

#         return response.Response({"transactions": serializer.data})
#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             data = serializer.validated_data
#             amount = str(data["amount"])
#             phonenumber = data["phone_number"]

#             # call stk_push from utils
#             try:
#                 response = stk_push(amount=amount, phonenumber=phonenumber)
#                 return Response(response, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
