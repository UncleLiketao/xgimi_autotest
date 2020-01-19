# API_AutoTest_Framework_HttpRunner


# API_Automation
## 执行用例

### 纯http
执行只含http接口的用例时，可使用
```bash
python ./httprunner/cli.py /path/to/testcase
```

### dubbo
执行带有dubbo接口的用例时，应使用
```bash
python ./httprunner/ext/dubbotelnet/cli.py /path/to/testcase
```