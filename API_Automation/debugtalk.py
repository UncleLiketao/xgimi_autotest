import json
import Aes_crypt

# 公共参数
commn_params = {
    'gimiPid': 'EHFAJEF79TAU', 'gimiDevice': 'aosp_synsepalum_YN', 'xgimiDeviceName': 'synsepalum_Y',
    'deviceMac': '80-0B-52-02-44-26', 'systemVersion': 'v1.6.23', 'launcherVersionCode': 1510,
}


def get_encrypt_data(data=None):
    """
    用于接口请求参数的加密处理，传入字典格式的参数，添加公共参数后一起加密后返回
    :param data: 传入的data为字典格式
    :return: requests_data 规定格式的Json数据
    """
    if data is None:
        data = {}
    for key in data.keys():
        commn_params[key] = data[key]
    before_encrypt_data = json.dumps(commn_params)
    params = Aes_crypt.AesCrypt().aes_encode(before_encrypt_data)
    requests_data = {"params": "%s" % params}
    return requests_data


def get_nonencrypt_data(data: dict):
    """
    用于接口请求的非加密参数处理，传入字典格式的参数
    :param data:
    :return: requests_data 规定格式的Json数据
    """
    requests_data = {"params": "%s" % json.dumps(data)}
    return requests_data


# 实例
print(get_encrypt_data({"broadcastScene": "1"}))
print(get_nonencrypt_data({"sourceId": "10001", "sourceType": 2}))
