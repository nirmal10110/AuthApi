import os
from typing import Dict
from cryptography.fernet import Fernet

# key = os.environ.get("WALLET_KEY")
key = "IdEsC3I1R9ZJDp0PmHtFXWkIWJq7ACJCrqRsZubVEOM="


class Decryption:
    @classmethod
    def decrypt_response(cls, data: Dict):
        # print(data)
        f = Fernet(key)
        decrypted_data = {}
        for i in data:
            decrypted_data[i] = \
                f.decrypt(bytes(data[i], 'ascii')).decode('ascii')
        # print(decrypted_data)
        return decrypted_data
