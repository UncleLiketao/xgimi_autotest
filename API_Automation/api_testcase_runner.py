import requests
import os
import numpy

email_sender_url = "http://notify.i.xgimi.com/notification/email/send"


def get_report():
    files_list = []
    file_path = "C:\\Users\jeremy.li\PycharmProjects\\xgimi_autotest\API_Automation\\reports"
    for root, dirs, files in os.walk(file_path):
        print(root)
        print(dirs)
        print(files)


def send_email(toEmaiList, app_id, report_path):
    receiver_list = get_toEmaiList()
    print(receiver_list)
    # html_file_path = "C:\\Users\jeremy.li\PycharmProjects\\xgimi_autotest\API_Automation\\reports\\1574145534.html"
    # with open(html_file_path, "r", encoding="utf-8") as f:
    #     file = f.read()
    # req_data = {"toEmailList": ["jeremy.li@xgimi.com",], "subject": "Launcher3.0 接口自动化测试邮件",
    #             "content": file}
    # req_data_json = json.dumps(req_data)
    # res = requests.post(pre_env_sender, data=req_data_json)
    # print(res.status_code)


def get_toEmaiList():
    res = requests.get("http://devops.t.xgimi.com/apis/project/monitor?name=%s" % "gossapi网关")
    res_dict = res.json()
    receiver_list = res_dict['data']['data'][0]['notifications'].split("|")
    for num in range(len(receiver_list)):
        receiver_list[num] = receiver_list[num] + "@xgimi.com"
    return receiver_list


def run_case():
    os.chdir("C:\\Users\jeremy.li\PycharmProjects\\xgimi_autotest\API_Automation")
    print(os.getcwd())
    os.system("hrun testcases")


if __name__=='__main__':
    get_report()
    # send_email()
    # get_receiver()
    # run_case()
