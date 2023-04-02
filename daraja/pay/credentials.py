import base64
import json
from datetime import datetime

import requests


class c2bCredentials:
    consumer_key = 'CONSUMER_KEY'
    consumer_secret = 'CONSUMER_SECRET'
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class accessToken:
    req = requests.get(c2bCredentials.api_url, auth=(c2bCredentials.consumer_key, c2bCredentials.consumer_secret))
    mpesaAccessToken = json.loads(req.text)
    validToken = mpesaAccessToken['access_token']


class mpesaPassword:
    pay_time = datetime.now().strftime('%Y%m%d%H%M%S')
    shortCode = "174379"
    Test_c2b_shortcode = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    dataToEncode = shortCode + passkey + pay_time
    onlinePassword = base64.b64encode(dataToEncode.encode())
    decodePassword = onlinePassword.decode('utf-8')
