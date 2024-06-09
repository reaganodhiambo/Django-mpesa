import os
import json
import base64
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


class c2bCredentials:
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_url = os.getenv('api_url')


class accessToken:
    req = requests.get(c2bCredentials.api_url, auth=(c2bCredentials.consumer_key, c2bCredentials.consumer_secret))
    mpesaAccessToken = json.loads(req.text)
    validToken = mpesaAccessToken['access_token']


class mpesaPassword:
    pay_time = datetime.now().strftime('%Y%m%d%H%M%S')
    shortCode = "174379"
    Test_c2b_shortcode = "174379"
    passkey = os.envget('passkey')

    dataToEncode = shortCode + passkey + pay_time
    onlinePassword = base64.b64encode(dataToEncode.encode())
    decodePassword = onlinePassword.decode('utf-8')
