import requests

base_url = 'http://127.0.0.1:5000/wallet'
url_get_amount = "/payamount"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
timeout = 10


class Wallet:

    @classmethod
    def authorize(cls, mobile_number: str):
        url = base_url
        payload = {
            "mobile_number": mobile_number
        }
        try:
            response = requests.get(url, json=payload, headers=headers, timeout=timeout)
        except:
            return None

        return response

    @classmethod
    def get_amount(cls, mobile_number: str, amount: int):
        url = base_url + url_get_amount
        payload = {
            "mobile_number": mobile_number,
            "amount": amount
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)
        except:
            return None

        return response