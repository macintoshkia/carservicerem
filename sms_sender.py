import os
import requests

def send_sms(phone_number, message):
    api_key = os.getenv("FARAZSMS_API_KEY", "YOUR_API_KEY")
    payload = {
        "api_key": api_key,
        "to": phone_number,
        "message": message
    }
    # Replace with real endpoint and headers if needed
    response = requests.post("https://api.farazsms.com/sms", json=payload)
    return response.status_code == 200