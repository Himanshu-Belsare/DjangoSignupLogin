from django.conf import settings
import requests

def send_otp(mobile_number,otp):
    urls = f"https://2factor.in/API/v1/{settings.API_KEY}/SMS/{mobile_number}/{otp}/Yout otp is"
    payload = ""
    headers = {"content-type":"application/x-www-form-urlencoded"}
    response = requests.get(url=urls,data=payload,headers=headers)
    breakpoint()
    print(response.text)
    return bool(response.ok)
