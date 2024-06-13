from django.core.exceptions import ValidationError
def validate_phone_number():
    """A very Basic validation to remove the preceding + or replace the 0 with 254"""
    if phone_number[0] == "+":
        phone_number = phone_number[1:]
    if phone_number[0] == "0":
        phone_number = "254" + phone_number[1:]
    return phone_number
