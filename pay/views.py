import json
import requests
# from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from .credentials import accessToken, mpesaPassword
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponse("Mpesa Daraja Home Page")


# STK Push to phone number
@csrf_exempt
def lipaNaMpesa(request):
    # stk push to client
    lipa_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {"Content-Type": "application/json"}
    headers.update({'Authorization': 'Bearer {0}'.format(accessToken.validToken)})
    payload = {
        "BusinessShortCode": mpesaPassword.shortCode,
        "Password": "{0}".format(mpesaPassword.decodePassword),
        "Timestamp": "{0}".format(mpesaPassword.pay_time),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254708374149,
        "PartyB": int(mpesaPassword.shortCode),
        "PhoneNumber": 254708374149,
        "CallBackURL": "https://e847-197-248-74-179.eu.ngrok.io/api/payments/lnm/",
        "AccountReference": "SuperBridge",
        "TransactionDesc": "Payment of Test"
    }
    response = requests.post(lipa_url, json=payload, headers=headers)

    return HttpResponse(response)



def c2b(request):
    headers = {}
    headers.update({'Authorization': 'Bearer {0}'.format(accessToken.validToken)})

    payload = {
        "ShortCode": 600992,
        "ConfirmationURL": "https://e847-197-248-74-179.eu.ngrok.io/api/payments/lnm/",
        "ValidationURL": "https://e847-197-248-74-179.eu.ngrok.io/api/payments/lnm/",
        "ResponseType": "Completed",

    }

    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl', headers=headers,json=payload)
    return HttpResponse(response.text)

def new(request):
    url7 = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    headers = {}
    headers.update({'Authorization': 'Bearer {0}'.format(accessToken.validToken)})
    payload = {
        "ShortCode": 600992,
        "CommandID": "CustomerBuyGoodsOnline",
        "Amount": 1,
        "Msisdn": 254748792401,
        "BillRefNumber": "null",
    }

    response = requests.post(url7, json=payload, headers=headers)
    return  HttpResponse(response)

@csrf_exempt
def confirmation(request):
    mpesa_body =request.body
    print(mpesa_body)
    return HttpResponse(mpesa_body)


@csrf_exempt
def validation(request):
    print('validate')
    vall = request.body
    return HttpResponse(vall)

