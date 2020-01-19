# -*- coding: utf-8 -*-
"""telnet方式请求dubbo接口的封装
"""

from telnetlib import Telnet
import re
import json
from json import JSONDecodeError


class Dubbo:

    PROMPT = "dubbo>"

    def __init__(self, host:str="", port:int=-1, timeout=5):
        self._host = host
        self._port = port
        self._timeout = timeout

    def invoke(self, service, method, params=""):
        """invode dubbo method

        Args:
            service(string): service path
            method(string): method name
            params(dict): params of the method
        
        Returns:
            The return of the requested method(an object extracted from json)
        
        Raises:
            socket.timeout
        """
        if not self._host or int(self._port) < 0:
            raise AttributeError("Host or port has not been set.")

        if service:
            command = "invoke {}.{}({})\n".format(service, method, params)
        else:
            command = "invoke {}({})\n".format(method, params)

        with Telnet(self._host, self._port, self._timeout) as tn:
            tn.write(command.encode())
            rt = tn.read_until(self.PROMPT.encode())

        # extract json data
        raw_data = rt.decode()
        # TODO: Refactor the regex
        regex = "({}\\n\\r\\.sm \\d* :despale\\n\\r)(.*)".format(self.PROMPT[::-1])
        result = re.match(regex, raw_data[::-1], flags=re.DOTALL)

        json_object = {"code": "extract error: raw_data", "data": raw_data}
        if result:
            json_data = result.group(2)[::-1]
            try:
                json_object = json.loads(json_data)
            except JSONDecodeError:
                json_object = {"code": "extract error: raw_data", "data": json_data}

        return json_object

    def set_host(self, host, port):
        self._host = host
        self._port = port
    
    # TODO: log level settings and output debug message


class DubboContext:
    pass


if __name__ == "__main__":

    ip = "10.40.33.172"
    port = 20107
    dubbo = Dubbo(ip, port)

    service = ""
    method = "getWeatherCities"
    rt = dubbo.invoke(service, method)
    print(rt)
