import json
import Aes_crypt

commn_params = {
    'gimiPid': 'EHFAJEF79TAU', 'gimiDevice': 'aosp_synsepalum_YN', 'xgimiDeviceName': 'synsepalum_Y',
    'deviceMac': '80-0B-52-02-44-26', 'systemVersion': 'v1.6.23', 'launcherVersionCode': 1510,
}


def get_encrypt_data(data=None):
    if data is None:
        data = {}
    for key in data.keys():
        commn_params[key] = data[key]
    before_encrypt_data = json.dumps(commn_params)
    params = Aes_crypt.AesCrypt().aes_encode(before_encrypt_data)
    requests_data = {"params": "%s" % params}
    return requests_data


def get_nonencrypt_data(data: dict):
    requests_data = {"params": "%s" % json.dumps(data)}
    return requests_data


print(get_encrypt_data({"broadcastScene":"1"}))
print(get_nonencrypt_data({"sourceId":"10001","sourceType":2}))