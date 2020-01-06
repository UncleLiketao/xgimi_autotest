from .dubbo_telnet import Dubbo
import time
from socket import timeout
import jsonpath
import re
import sys, os
import copy
from collections import OrderedDict

from httprunner.client import ApiResponse
from httprunner.response import ResponseObject
from httprunner import exceptions, logger, utils
from httprunner.compat import basestring, is_py2


text_extractor_regexp_compile = re.compile(r".*\(.*\).*")

########################
# client               #
########################
class DubboApiResponse(ApiResponse):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def raise_for_status(self):
        """override
        """
        if hasattr(self, 'error') and self.error:
            raise self.error

class DubboSession():
    """Artificial class for httprunner.client.HttpSession

    Class for performing dubbo requests and holding request and response data
    between requests(teststeps).
    Each request is logged so that HttpRunner can display statistics.
    """

    def __init__(self):
        self._dubbo = Dubbo(timeout=3)
        self.init_meta_data()
        self.response_list = []

    def init_meta_data(self):
        """ initialize meta_data, it will store detail data of request and response
        """
        self.meta_data = {
            "name": "",
            "interface_type": "dubbo",  # 作为dubbo类型接口的标识，用于模板渲染
            "data": [
                {
                    "request": {
                        "host": "N/A",
                        "port": -1,
                        "service": "N/A",
                        "method": "N/A",
                        "params": {}
                    },
                    # TODO: structure of response
                    "response": {
                        "status_code": "N/A",
                        "headers": {},
                        "encoding": None,
                        "content_type": ""
                    }
                }
            ],
            "stat": {
                "content_size": "N/A",
                "response_time_ms": "N/A",
                "elapsed_ms": "N/A",
            }
        }

    def update_last_req_resp_record(self, resp_obj):
        """
        update request and response info from Response() object.
        """
        self.meta_data["data"].pop()
        self.meta_data["data"].append(self.get_req_resp_record(resp_obj))

    @staticmethod
    def get_req_resp_record(resp_obj):
        """ get request and response info from Response() object.
        """
        def log_print(req_resp_dict, r_type):
            msg = "\n================== {} details ==================\n".format(
                r_type)
            for key, value in req_resp_dict[r_type].items():
                msg += "{:<16} : {}\n".format(key, repr(value))
            logger.log_debug(msg)

        req_resp_dict = {
            "request": {},
            "response": {}
        }
        # log request details in debug mode
        if isinstance(resp_obj, DubboApiResponse):
            req_resp_dict["request"] = copy.copy(resp_obj.kwargs)
        elif isinstance(resp_obj, dict):
            req_resp_dict["request"] = copy.copy(resp_obj.get("request"))
        else:
            pass # TODO
        log_print(req_resp_dict, "request")

        # log response details in debug mode
        if isinstance(resp_obj, DubboResponseObject):
            req_resp_dict["response"]["body"] = resp_obj.json
        elif isinstance(resp_obj, dict):
            req_resp_dict["response"]["body"] = resp_obj["body"]
        else:
            req_resp_dict["response"]["body"] = resp_obj.error
        log_print(req_resp_dict, "response")

        return req_resp_dict

    def request(self, host, port, service, method, params="", name=None, **kwargs):
        """
        Send a request to the dubbo server and return its result.

        TODO
        Args:
            host(str): ip or url
            port(int): dubbo service port
            service(str): the service to request
            method(str): the method to request
            params(dict): params the method need

        TODO: doc
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        self.init_meta_data()

        # record test name
        self.meta_data["name"] = name

        # record original request info
        self.meta_data["data"][0]["request"]["service"] = service
        self.meta_data["data"][0]["request"]["method"] = method

        # TODO: 可选参数的设计
        # kwargs.setdefault("timeout", 120)
        # self.meta_data["data"][0]["request"].update(kwargs)

        start_timestamp = time.time()
        response = self._send_request_safe_mode(
            host, port, service, method, params, **kwargs)
        response_time_ms = round((time.time() - start_timestamp) * 1000, 2)
        if isinstance(response, dict):
            response_length = len(str(response.get("body", "")))
        else:
            response_length = -1

        # TODO: 可选参数设计
        # # get the length of the content, but if the argument stream is set to True, we take
        # # the size from the content-length header, in order to not trigger fetching of the body
        # if kwargs.get("stream", False):
        #     content_size = int(dict(response.headers).get("content-length") or 0)
        # else:
        #     content_size = len(response.content or "")

        # record the consumed time
        self.meta_data["stat"] = {
            "response_time_ms": response_time_ms,
            "elapsed_ms": response_time_ms,
            "content_size": response_length
        }

        # record request and response histories, include 30X redirection
        self.response_list.append(response)
        self.meta_data["data"] = [
            self.get_req_resp_record(resp_obj)
            for resp_obj in self.response_list
        ]

        # TODO
        try:
            if isinstance(response, DubboApiResponse):
                response.raise_for_status()
        except timeout as e:
            logger.log_error(u"{exception}".format(exception=str(e)))
        else:
            logger.log_info(
                """, response_time(ms): {} ms, response_length: {} bytes\n""".format(
                    response_time_ms, response_length
                )
            )

        return response

    def _send_request_safe_mode(self, host, port, service, method, params, **kwargs):
        """
        Send a dubbo request
        TODO: 设计可选参数，设计ApiResponse使用例出现问题后处理不出错
        """
        meta_data = {
            "host": host,
            "port": port,
            "service": service,
            "method": method,
            "params": params,
        }
        try:
            msg = "processed request:\n"
            msg += "> {service}.{method}\n".format(service=service, method=method)
            msg += "> params: {params}".format(params=params)
            self._dubbo.set_host(host, port)
            response_data = self._dubbo.invoke(service, method, params)
            response = {
                "body": response_data,
                "request": {
                    "host": host,
                    "port": port,
                    "service": service,
                    "method": method
                    }
                }
        except timeout as e:
            logger.log_error("{exception}".format(exception=str(e)))
            response = DubboApiResponse(**meta_data)
            response.error = e
        except Exception as e:
            logger.log_info(
                "something unknown happened while requesting {}.{}".format(service, method))
            response = DubboApiResponse(**meta_data)
            response.error = e
        return response

########################
# response             #
########################
class DubboResponseObject(ResponseObject):
    """Artificial class for httprunner.response.ResponseObject
    """
    def __getattr__(self, key):
        """override
        """
        try:
            if key == "json":
                value = self.resp_obj["body"]
            elif key == "status_code":
                value = self.resp_obj["body"]["code"]
            else:
                value = getattr(self.resp_obj, key)

            self.__dict__[key] = value
            return value
        except AttributeError:
            err_msg = "DubboResponseObject does not have attribute: {}".format(key)
            logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)
