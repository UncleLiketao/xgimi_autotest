import flask, json
from flask import request
from API_Automation.api_testcase_runner import main

"""
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
登录接口，需要传url、username、passwd
"""
server = flask.Flask(__name__)


# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式
@server.route('/runcase', methods=['get', 'post'])
def runcase():
    # 获取通过url请求传参的数据
    app_id = request.values.get('app_id')
    # 判断用户名、密码都不为空，如果不传用户名、密码则username和pwd为None
    if app_id:
        if app_id == 'testcases':
            resu = {'code': 200, 'message': '请求成功', '测试应用': "%s" % app_id}
            main()
            return json.dumps(resu, ensure_ascii=False)  # 将字典转换为json串, json是字符串

        else:
            resu = {'code': -1, 'message': 'APP_ID不在配置范围内'}
            return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 10001, 'message': 'APP_ID参数不能为空！'}
        return json.dumps(resu, ensure_ascii=False)


if __name__=='__main__':
    server.run(debug=True, port=8888, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
