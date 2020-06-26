import json
import requests
from libs.encryption import Encryption

port = 'https://wallet-api-v1.herokuapp.com'
url_details = "/wallet"
url_get_amount = "/wallet/amount"
url_add_amount = "/wallet/add/amount"

headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
timeout = 10


class Wallet:

    def authorize(self, mobile_number: str):
        payload = {
            "mobile_number": mobile_number
        }
        # payload = json.dumps(Encryption.encrypt(payload))
        url = port + url_details 

        try:
            response_get = requests.get(url, json=payload, headers=headers, timeout=timeout)
        except:
            return None
        return response_get
        
    def get_amount(self, mobile_number: str, amount: float):
        url = port+url_get_amount
        payload = {
            "mobile_number": mobile_number,
            "amount": amount
        }
        # payload = json.dumps(Encryption.encrypt(payload))
        try:
            response_amount = requests.put(url, json=payload, headers=headers, timeout=timeout)
        except:
            return None
        
        return response_amount
    
    def send_amount(self, mobile_number: str, amount: float):
        url = port+url_add_amount
        payload = {
            "mobile_number": mobile_number,
            "amount": amount
        }
        # payload = json.dumps(Encryption.encrypt(payload))
        try:
            response_amount = requests.put(url, json=payload, headers=headers, timeout=timeout)
        except:
            return None
        # print(response_amount.text,response_amount.status_code)
        return response_amount