from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import stk_push
from .models import Transation, ResponseBody
from .serializers import TransactionSerializer, ResponseBodySerializer, StkPushSerializer

# Create your views here.
class StkPushView(APIView):
    """
    View to send stk push to user
    Takes amount and phonenumber as arguments for the stk_push
    function
    """
    def post(self,request):
        serializer = StkPushSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(response,status=status.HTTP_200_OK,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallbackView(APIView):
    """
    View to handle Mpesa callback data and transaction management.
    gets the response json and creates a new object
    """

    def post(self, request,format=None):
        print("start")
        body = request.data
        if body:
            mpesa = ResponseBody.objects.create(body=body)
            mpesa_data = mpesa.body
            if mpesa_data['Body']['stkCallback']['ResultCode'] == 0:
                transaction = Transation.objects.create(
                    phone_number=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
                    amount=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
                    receipt_no=mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"]
                )
                print(mpesa_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"])
                return Response({"Transaction Successfull":transaction}, status=status.HTTP_201_CREATED)

            # cancelled transaction
            elif mpesa_data['Body']['stkCallback']['ResultCode'] == 1032:
                ErrorDesc=mpesa_data['Body']['stkCallback']['ResultDesc']
                print(ErrorDesc)
                return Response({"Error":ErrorDesc},status=status.HTTP_200_OK)

            else:
                return Response(
                    {"message": "Something went wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        print("errorrr")
        return Response(
            {"error": "Mpesa Callback processing failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        response = ResponseBody.objects.all()
        serializer = ResponseBodySerializer(response,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
