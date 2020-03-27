import json
import Aes_crypt
import random
from jsonschema import validate
import json


# 辅助工具
def errortracker(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print("Error in {}".format(func.__name__))
            raise

    return wrapper


# 基础工具
def random_seq(length):
    """获取随机序列

    Args:
        length: 序列长度

    Returns:
        随机序列
    """
    pass


def random_randint(*args, **kwargs):
    """random.randint的封装
    """
    return random.randint(*args, **kwargs)


@errortracker
def random_choice(choices, attributes=None):
    """random.choice的封装与扩展，可传入attributes向下取其属性

    Args:
        choices: 输入的列表
        attributes: 字符串，需要取的属性名，向下取多层时以'.'分隔，为None时不取
            e.g.
                "data.id" 表示取 choice["data"]["id"]

    Returns:
        随机选择的元素的特定属性
    """
    choice = random.choice(choices)
    if attributes is None:
        return choice
    stack = attributes.split('.')
    for attribute in stack:
        choice = choice.get(attribute)
    return choice


def random_list(func_name, length, *args, **kwargs):
    """使用func_name返回值作为list元素生成随机列表
    旨在生成数据驱动测试的数据

    Args:
        func_name: 生成单个元素使用的函数名
        length: 列表长度
        *args, **kwargs: func_name所需的参数
    
    Returns:
        随机生成的列表
    """
    return [eval("{}(*{}, **{})".format(func_name, args, kwargs)) for _ in range(length)]


def printOK():
    print("OK")


# teststep teardown hooks
def teardown_hook_validate_jsonschema(response, schema_path):
    print("validating...")
    with open(schema_path, 'r') as schema_fd:
        schema = json.load(schema_fd) # TODO
        content = json.loads(response.content)
        validate(content, schema)


# 不同应用的公共参数
Launcher_common_params = {
    'gimiPid': 'EHFAJEF79TAU', 'gimiDevice': 'aosp_synsepalum_YN', 'xgimiDeviceName': 'synsepalum_Y',
    'deviceMac': '80-0B-52-02-44-26', 'systemVersion': 'v1.6.23', 'launcherVersionCode': 1510,
}
app4_common_params = {
    "gimiPid": "EHFAJEF79TAU", "gimiDevice": "aosp_bennet_polo", "xgimiDeviceName": "synsepalum_Y",
    "deviceMac": "80-0B-52-02-44-26", "systemVersion": "v1.6.23", "uiVersion": 1510,
    "appName": "Android 6.0", "appVersion": 1510, "mProductId": 5997, "mVendorId": 7006
}
NewUI_GossApi_common_params = {
    "gimiPid": "DSFASKDFASD2",
    "xgimiDeviceName": "Product_z6b",
    "gimiDevice": "Product_z6b",
    "launcherVersionCode": 1,
    "deviceMac": "00:0B:52:12:02:DB",
    "systemVersion": "v12.2.69"
}

# 加密解密
def get_encrypt_data(data=None, common_params_type=None):
    """
    用于接口请求参数的加密处理，传入字典格式的参数，添加公共参数后一起加密后返回
    :param data: 传入的data为字典格式
    :return: requests_data 规定格式的Json数据
    """
    common_params = {}
    if data is None:
        data = {}
    if common_params_type == "Launcher_common_params":
        common_params = Launcher_common_params
    elif common_params_type == "app4_common_params":
        common_params = app4_common_params
    elif common_params_type == "NewUI_GossApi_common_params":
        common_params = NewUI_GossApi_common_params
    for key in data.keys():
        common_params[key] = data[key]
    before_encrypt_data = json.dumps(common_params)
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
def get_data(data: dict):
    requests_data = json.dumps(data)
    return requests_data
# 实例
# print(get_encrypt_data({"broadcastScene": "1",}, "app4_common_params"))
# print(get_nonencrypt_data({"sourceId": "10001", "sourceType": 2}))
