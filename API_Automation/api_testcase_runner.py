import requests
import shutil
import os
import json

# 项目根目录路径
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), '.'))
# 获取发布系统项目发布项目通知人员信息接口路径（正式环境）
APIS_PROJECT_MONITOR_URL = "http://devops.t.xgimi.com/apis/project/monitor"
# 接口测试根目录
API_AUTOMATION_PATH = PROJECT_PATH + "\\API_Automation"
# 接口测试报告路径
API_REPORT_PATH = PROJECT_PATH + "\\API_Automation\\reports"
# OA邮件发送接口生产环境地址
EMAIL_SENDER_URL = "http://notify.i.xgimi.com/notification/email/send"


def get_toEmaiList(app_id="gossapi网关"):
    """
    通过DevOps接口获取发布系统发布项目通知人员信息
    :param app_id: 发布系统的项目名称
    :return:toEmaiList 通知人员极米邮箱列表
    """
    r = requests.get(APIS_PROJECT_MONITOR_URL + "?name=" + app_id)
    r_json = r.json()
    toEmaiList = r_json['data']['data'][0]['notifications'].split("|")
    for i in range(len(toEmaiList)):
        toEmaiList[i] = toEmaiList[i] + "@xgimi.com"
    print("邮件发送项目为：" + app_id + "\n" + "邮件发送人员名单：" + str(toEmaiList))
    return toEmaiList


def run_case(case_path="testcases"):
    """
    根据传入的app_id来确定需要执行的测试用例，执行前先清空以往的测试报告保证测试报告的唯一性
    :param case_path:
    :return:
    """
    shutil.rmtree(API_REPORT_PATH)
    os.chdir(API_AUTOMATION_PATH)
    print(os.getcwd())
    os.system("hrun" + " " + case_path)


def send_email(toEmailList):
    """
    使用通知服务接口发送测试报告到通知人员极米邮箱
    :return:
    """
    for dirpath, dirnames, filenames in os.walk(API_REPORT_PATH):
        for filepath in filenames:
            report_path = os.path.join(dirpath, filepath)
    print("测试报告地址为:" + report_path)
    with open(report_path, "r", encoding="utf-8") as f:
        file = f.read()
    email_data = {"toEmailList": toEmailList, "subject": "接口自动化测试邮件",
                  "content": file}
    send_email_response = requests.post(EMAIL_SENDER_URL, data=json.dumps(email_data))
    print(send_email_response.json())


def main():
    to_EmailList = get_toEmaiList()
    run_case()
    send_email(to_EmailList)


if __name__ == '__main__':
    main()