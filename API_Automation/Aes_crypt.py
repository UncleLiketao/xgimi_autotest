from Crypto.Cipher import AES
import base64


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
        while len(s) % 16 != 0:
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
    encrypt_data = "EYGJdmKfOXGe0JS3BAmlpAZSAypHuzesHHvKJBh5RXVXoSz/jrJUKCoujH+SOHXzLIGjJdB6562uYlTjHpbtf1h2Ov3h/xEC1b6GxXCN10YOUxipFRtIH8L53hv25Gt6VQQJND5Sp67Y4nEBvVhr9DRncyTU6VF3vlpleO08H+Dm2OjTysd7nRwi6UP4gVgJTekmUBigSQb3TIOVTRK5N6l4aF3yHXoLGnM6jShUTtLQ9ZQ+rlgsDSBAT6HN+1SWZuBuVoYzi9YNABPzwxU2ZPFYRZLMZhBQPW8pCQP7Z0OciL+h4RWMrJYPt6jbMgRKhHm7m33Hwjinj1xvfvbp/raT88H8XQBA6InOYOT/ZtDwpAEWm7nJzQg80zHm6XSa+qNctnaB00Wkp59LenNPeQ=="
    Query_data = {'gimiPid': 'EHFAJEF79TAU', 'gimiDevice': 'aosp_synsepalum_YN', 'xgimiDeviceName': 'synsepalum_Y',
                  'deviceMac': '80-0B-52-02-44-26', 'systemVersion': 'v1.6.23', 'launcherVersionCode': 1510,
                  'androidVersion': 'Android 6.0', 'systemIsRoot': False}
    aes = AesCrypt()
    print(aes.aes_decode(encrypt_data))
    # json_query_data = json.dumps(Query_data)
    # print(aes.aes_encode(json_query_data))
    # print(aes.aes_decode(aes.aes_encode(json_query_data)))

