from Crypto.Cipher import AES
import base64
import json


class AesCrypt(object):
    def __init__(self):
        self.key = "H9846F3UTOXBW05SIEGKD2CVQRJZLPAN"
        self.mode = AES.MODE_ECB
        self.cipher = AES.new(str.encode(self.key), self.mode)
        self.bs = AES.block_size
        self.pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    @staticmethod
    def add_to_16(s):
        while len(s) % 16!=0:
            s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
        return str.encode(s)

    # AES加密
    def aes_encode(self, msg):
        encrypted_text = str(base64.encodebytes(self.cipher.encrypt(self.add_to_16(msg))), encoding='utf8').replace(
            '\n', '')
        return encrypted_text

    # AES解密
    def aes_decode(self, encrypt_data):
        decrypted_text = self.cipher.decrypt(base64.decodebytes(bytes(encrypt_data, encoding='utf8'))).decode("utf8")
        return self.unpad(decrypted_text)


if __name__ == '__main__':
    aes = AesCrypt()
    method_choice = input("请输入您要进行的操作：1.解密 2.加密\n")
    if method_choice == "1":
        encrypt_data = input("请输入需要解密的内容：\n")
        print(aes.aes_decode(encrypt_data))
    elif method_choice == "2":
        query_data = input("请输入需要加密的内容：\n")
        json_query_data = json.dumps(query_data)
        print(aes.aes_encode(json_query_data))
