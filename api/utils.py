import os
import base64
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()


def generate_access_token():
    """
    uses your consumer key and consumer secret to generate
    access token used for authenticating all other API calls

    """
    access_token_url = os.getenv("ACCESS_TOKEN_URL")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")

    # combine consumer_key and consumer_secret then encode using b64
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(access_token_url, headers=headers)

    # if successfull return access_token from the json data
    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        return access_token

    else:
        raise Exception(f"Failed to generate access token: {response.text}")


def generate_password():
    """ """
    shortcode = os.getenv("SHORTCODE")
    passkey = os.getenv("PASSKEY")
    timestamp = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    password = shortcode + passkey + timestamp
    encoded_password = base64.b64encode(password.encode()).decode()
    return encoded_password


def stk_push(amount,phonenumber):
    """
    use the access token from generate_access_token to .....
    """

    access_token = generate_access_token()
    api_url = os.getenv("STKPUSH_URL")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "BusinessShortCode": os.getenv("SHORTCODE"),
        "Password": generate_password(),
        "Timestamp": f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phonenumber,
        "PartyB": 174379,
        "PhoneNumber": phonenumber,
        "CallBackURL": os.getenv("CALLBACK_URL"),
        "AccountReference": "Fadhelah",
        "TransactionDesc": "Nimemaliza",
    }

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data["CustomerMessage"])
        return data
    else:
        raise Exception(f"Failed to send STK push: {response.text}")

# stk_push(1,254759398194)