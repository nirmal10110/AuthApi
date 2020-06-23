import requests

port = 'https://wallet-api-v1.herokuapp.com/'
url_details = "wallet/"
url_get_amount = "wallet/getamount"

INTERNAL_SERVER_ERROR = 'INTERNAL SERVER ERROR'


class Wallet:

    def authorize(self, mobile_number: str):

        url = port + url_details + mobile_number
        try:
            response_get = requests.get(url)
        except:
            return None

        print(response_get.json())
        return response_get

    def get_amount(self, mobile_number: str, amount: int):
        url = port+url_get_amount
        payload = {
            "mobile_number": mobile_number,
            "amount": amount
        }
        try:
            response_amount = requests.put(url,
                                           json =payload)
            # print(response_amount.text)
        except:
            return None
        print(response_amount.text,response_amount.status_code)
        return response_amount
