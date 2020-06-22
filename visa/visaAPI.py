import requests
import pprint as pp
import os




userName = '8GFE0M5K05DRU333DPRB21haM32rE3BRpRxawIqOoTTlE1h78'
password = 'EhjXxl6b6'

certificatePath = './VisaCert/cert.pem'
privateKeyPath = './VisaCert/key_dc5f5933-d604-4b6f-a63a-136f20ee9892.pem'
caCertPath = "./VisaCert/server.pem"
path = os.path.abspath("server.pem")

# apiKey = 'I1SLOAJ5UMJKPLBRGDZG212UcGwVew8psy3O3HE9_32E8w-GA'
# sharedSecret = "Qi/5/eZheKoYiIWBFjz/5q5ylPH}}lUR2u4wcS0O"


url = "https://sandbox.api.visa.com/visadirect/mvisa/v1/merchantpushpayments"
# url_push_out = "https://sandbox.api.visa.com/visadirect/mvisa/v1/cashoutpushpayments"
headers = {'Accept': 'application/json'}
timeout = 10


class MVisa:

    @classmethod
    def cash_in_push_payments_post_payload(cls, payload):
        # print(payload)
        print(payload['localTransactionDateTime'])

        try:
            r = requests.post(url,
                              verify=(caCertPath),
                              cert=(certificatePath, privateKeyPath),
                              headers=headers,
                              auth=(userName, password),
                              #   data = body,
                              json=payload,
                              timeout=timeout)
            pp.pprint(r)
        except Exception as e:
            # raise(e)
            print(e)
            return None

            print(r.status_code)
            print(r.reason)
            # print(r.Respose)

            # print(r)
            # r = r.json()
            # pp.pprint(r)
        return r

    @classmethod
    def cash_in_push_payments_get_get_response(cls, status_identifier):

        url_merchant = url + '/' + status_identifier

        try:
            r = requests.post(url_merchant,
                              verify=(caCertPath),
                              cert=(certificatePath, privateKeyPath),
                              headers=headers,
                              auth=(userName, password),
                              #   data = body,
                              # json=payload,
                              timeout=timeout)

        except Exception as e:
            return e

        print(r.status_code)
        print(r.reason)
        # print(r.Respose)
        r = r.json()
        # print(r)
        pp.pprint(r)

        return r
