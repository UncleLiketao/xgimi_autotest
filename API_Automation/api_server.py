import flask, json
from flask import request
from API_Automation.api_testcase_runner import main

server = flask.Flask(__name__)


@server.route('/')
def hello_api():
    return "欢迎使用测试接口 \n 接口路径和需要传入参数如下："


# case运行API，需传入app_id
@server.route('/runcase', methods=['POST'])
def runcase():
    app_id = request.values.get('app_id')
    if app_id:
        if app_id == 'Launcher3.0接口':
            resu = {'code': 200, 'message': '请求成功', '测试应用': "%s" % app_id}
            main()
            return json.dumps(resu, ensure_ascii=False)

        else:
            resu = {'code': -1, 'message': 'APP_ID不在配置范围内'}
            return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 10001, 'message': 'APP_ID参数不能为空！'}
        return json.dumps(resu, ensure_ascii=False)


# 获取用例API，需传入app_id
@server.route('/get_testcase_list', methods=['GET'])
def get_testcase_list():
    app_id = request.values.get('app_id')
    if app_id == 'Launcher3.0接口':
        return "返回所有Launcher3.0需要执行的测试用例"


if __name__=='__main__':
    # 允许公网访问
    server.run(debug=False, port=8888, host='0.0.0.0')
