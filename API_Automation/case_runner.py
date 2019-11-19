import requests
import httprunner
import json
import os

def send_email():
    pro_env_sender = "http://notify.i.xgimi.com"
    pre_env_sender = "http://notify.pre.xgimi.com"
    dev_env_sender = "http://basic-service.t.xgimi.com:3030"

    req_data = {"toEmailList": ["jeremy.li@xgimi.com"], "subject": ["接口测试邮件"], "content": "test demo"}
    req_data_json = json.dumps(req_data)
    print(req_data_json)
    r = requests.post(pro_env_sender, req_data_json)
    print(r.status_code)
    print(r.json())

def run_case():
    os.chdir("C:\\Users\jeremy.li\PycharmProjects\API_AutoTest_Framework_HttpRunner")
    print(os.getcwd())
    os.system("hrun testcases")


if __name__ == '__main__':
    run_case()

