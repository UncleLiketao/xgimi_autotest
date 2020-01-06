# encoding: utf-8
from enum import Enum
from unittest.case import SkipTest

from .artificial import DubboSession, DubboResponseObject
import os
import sys
import time
import unittest

from httprunner import exceptions, logger, response, utils, parser
from httprunner.client import HttpSession
from httprunner.runner import Runner, HookTypeEnum
from httprunner.context import SessionContext
from httprunner.validator import Validator
from httprunner.utils import lower_dict_keys, omit_long_data
from httprunner.api import HttpRunner
from httprunner.report import HtmlTestResult


########################
# runner.py            #
########################
class DRunner(Runner):
    """ dubbo testcases runner.
    """

    def __init__(self, config, http_client_session=None, dubbo_client_session=None):
        """override

        run testcase or testsuite.

        Args:
            config (dict): testcase/testsuite config dict

                {
                    "name": "ABC",
                    "variables": {},
                    "setup_hooks", [],
                    "teardown_hooks", []
                }

            http_client_session (instance): HttpSession().

        """
        self.dubbo_client_session = dubbo_client_session or DubboSession()
        super(DRunner, self).__init__(config, http_client_session)

    def __clear_test_data(self):
        """override

        clear request and response data
        """
        if isinstance(self.http_client_session, HttpSession):
            self.http_client_session.init_meta_data()

        if isinstance(self.dubbo_client_session, DubboSession):
            self.dubbo_client_session.init_meta_data()

    def _run_http_test(self, test_dict):
        """override
        """
        return self._run_test(test_dict)

    def _run_dubbo_test(self, test_dict):
        # parse test request
        raw_request = test_dict.get('request', {})
        parsed_test_request = self.session_context.eval_content(raw_request)
        self.session_context.update_test_variables(
            "request", parsed_test_request)

        # prepend url with base_url unless it's already an absolute URL
        host = parsed_test_request.pop('host', '')
        port = parsed_test_request.pop('port', '')

        # setup hooks
        setup_hooks = test_dict.get("setup_hooks", [])
        if setup_hooks:
            self.do_hook_actions(setup_hooks, HookTypeEnum.SETUP)

        try:
            service = parsed_test_request.pop('service')
            method = parsed_test_request.pop('method')
            params = parsed_test_request.pop("params", "")
            parsed_test_request.setdefault("verify", self.verify)
            group_name = parsed_test_request.pop("group", None)
        except KeyError:
            raise exceptions.ParamsError("SERVICE or METHOD missed!")

        logger.log_info(
            "{host}:{port} {service}.{method}".format(
                host=host, port=port, service=service, method=method
            )
        )
        logger.log_debug(
            "request kwargs(raw): {kwargs}".format(kwargs=parsed_test_request))

        # request
        resp = self.dubbo_client_session.request(
            host,
            port,
            service,
            method,
            params,
            name=(group_name or self.session_context.eval_content(
                test_dict.get("name", ""))),
            **parsed_test_request
        )
        # TODO: responseObject
        resp_obj = DubboResponseObject(resp)

        def log_req_resp_details():
            err_msg = "{} DETAILED REQUEST & RESPONSE {}\n".format(
                "*" * 32, "*" * 32)

            # log request
            err_msg += "====== request details ======\n"
            err_msg += "host: {}\n".format(host)
            err_msg += "port: {}\n".format(port)
            err_msg += "service: {}\n".format(service)
            err_msg += "method: {}\n".format(method)
            err_msg += "params: {}\n".format(params)
            for k, v in parsed_test_request.items():
                v = utils.omit_long_data(v)
                err_msg += "{}: {}\n".format(k, repr(v))

            err_msg += "\n"

            # log response
            err_msg += "====== response details ======\n"
            err_msg += "body: {}\n".format(repr(resp_obj.json))
            logger.log_error(err_msg)

        # teardown hooks
        teardown_hooks = test_dict.get("teardown_hooks", [])
        if teardown_hooks:
            self.session_context.update_test_variables("response", resp_obj)
            self.do_hook_actions(teardown_hooks, HookTypeEnum.TEARDOWN)
            self.dubbo_client_session.update_last_req_resp_record(resp_obj)

        # extract
        extractors = test_dict.get("extract", {})
        try:
            extracted_variables_mapping = resp_obj.extract_response(extractors)
            self.session_context.update_session_variables(
                extracted_variables_mapping)
        except (exceptions.ParamsError, exceptions.ExtractFailure):
            log_req_resp_details()
            raise

        # validate
        validators = test_dict.get(
            "validate") or test_dict.get("validators") or []
        validate_script = test_dict.get("validate_script", [])
        if validate_script:
            validators.append({
                "type": "python_script",
                "script": validate_script
            })

        validator = Validator(self.session_context, resp_obj)
        try:
            validator.validate(validators)
        except exceptions.ValidationFailure:
            log_req_resp_details()
            raise

        return validator.validation_results

    def _run_single_test(self, test_dict):
        """ override
        run single teststep.

        Args:
            test_dict (dict): teststep info
                {
                    "name": "teststep description",
                    "skip": "skip this test unconditionally",
                    "times": 3,
                    "interface_type": "dubbo"
                    "variables": [],            # optional, override
                    "request": {
                        "url": "http://127.0.0.1:5000/api/users/1000",
                        "method": "POST",
                        "headers": {
                            "Content-Type": "application/json",
                            "authorization": "$authorization",
                            "random": "$random"
                        },
                        "json": {"name": "user", "password": "123456"}
                    },
                    "extract": {},              # optional
                    "validate": [],             # optional
                    "setup_hooks": [],          # optional
                    "teardown_hooks": []        # optional
                }

        Raises:
            exceptions.ParamsError
            exceptions.ValidationFailure
            exceptions.ExtractFailure

        """

        # prepare
        test_dict = utils.lower_test_dict_keys(test_dict)
        interface_type = test_dict.get('interface_type', '')

        if interface_type == "dubbo":
            result = self._run_dubbo_test(test_dict)
        else:
            result = self._run_http_test(test_dict)

        return result

    def run_test(self, test_dict):
        """ run single teststep of testcase.
            test_dict may be in 3 types.

        Args:
            test_dict (dict):

                # teststep
                {
                    "name": "teststep description",
                    "variables": [],        # optional
                    "request": {
                        "url": "http://127.0.0.1:5000/api/users/1000",
                        "method": "GET"
                    }
                }

                # nested testcase
                {
                    "config": {...},
                    "teststeps": [
                        {...},
                        {...}
                    ]
                }

                # TODO: function
                {
                    "name": "exec function",
                    "function": "${func()}"
                }

        """
        self.meta_datas = None
        if "teststeps" in test_dict:
            # nested testcase
            test_dict.setdefault("config", {}).setdefault("variables", {})
            test_dict["config"]["variables"].update(
                self.session_context.session_variables_mapping)
            self._run_testcase(test_dict)
        else:
            # api
            validation_results = {}
            try:
                validation_results = self._run_single_test(test_dict)
            except Exception as e:
                # log exception request_type and name for locust stat
                self.exception_request_type = test_dict["request"]["method"]
                self.exception_name = test_dict.get("name")
                raise
            finally:
                # get request/response data and validate results
                if test_dict.get("interface_type", "") == "dubbo":
                    self.meta_datas = getattr(
                        self.dubbo_client_session, "meta_data", {})
                else:
                    self.meta_datas = getattr(
                        self.http_client_session, "meta_data", {})
                self.meta_datas["validators"] = validation_results

    def _run_testcase(self, testcase_dict):
        """override
        
        run single testcase.
        """
        self.meta_datas = []
        config = testcase_dict.get("config", {})

        # each teststeps in one testcase (YAML/JSON) share the same session.
        # 此处修改点
        test_runner = DRunner(
            config, self.http_client_session, self.dubbo_client_session)

        tests = testcase_dict.get("teststeps", [])

        for index, test_dict in enumerate(tests):

            # override current teststep variables with former testcase output variables
            former_output_variables = self.session_context.test_variables_mapping
            if former_output_variables:
                test_dict.setdefault("variables", {})
                test_dict["variables"].update(former_output_variables)

            try:
                test_runner.run_test(test_dict)
            except Exception:
                # log exception request_type and name for locust stat
                self.exception_request_type = test_runner.exception_request_type
                self.exception_name = test_runner.exception_name
                raise
            finally:
                _meta_datas = test_runner.meta_datas
                self.meta_datas.append(_meta_datas)

        self.session_context.update_session_variables(
            test_runner.export_variables(test_runner.export)
        )

########################
# api.py               #
########################


class DubboRunner(HttpRunner):

    def _add_tests(self, testcases):
        """override
        """
        def _add_test(test_runner, test_dict):
            """ add test to testcase.
            """

            def test(self):
                try:
                    test_runner.run_test(test_dict)
                except exceptions.MyBaseFailure as ex:
                    self.fail(str(ex))
                finally:
                    self.meta_datas = test_runner.meta_datas

            if "config" in test_dict:
                # run nested testcase
                test.__doc__ = test_dict["config"].get("name")
                variables = test_dict["config"].get("variables", {})
            else:
                # run api test
                test.__doc__ = test_dict.get("name")
                variables = test_dict.get("variables", {})

            if isinstance(test.__doc__, parser.LazyString):
                try:
                    parsed_variables = parser.parse_variables_mapping(
                        variables)
                    test.__doc__ = parser.parse_lazy_data(
                        test.__doc__, parsed_variables
                    )
                except exceptions.VariableNotFound:
                    test.__doc__ = str(test.__doc__)

            return test

        test_suite = unittest.TestSuite()
        for testcase in testcases:
            config = testcase.get("config", {})
            test_runner = DRunner(config)
            TestSequense = type('TestSequense', (unittest.TestCase,), {})

            tests = testcase.get("teststeps", [])
            for index, test_dict in enumerate(tests):
                times = test_dict.get("times", 1)
                try:
                    times = int(times)
                except ValueError:
                    raise exceptions.ParamsError(
                        "times should be digit, given: {}".format(times))

                for times_index in range(times):
                    # suppose one testcase should not have more than 9999 steps,
                    # and one step should not run more than 999 times.
                    test_method_name = 'test_{:04}_{:03}'.format(
                        index, times_index)
                    test_method = _add_test(test_runner, test_dict)
                    setattr(TestSequense, test_method_name, test_method)

            loaded_testcase = self.test_loader.loadTestsFromTestCase(
                TestSequense)
            setattr(loaded_testcase, "config", config)
            setattr(loaded_testcase, "teststeps", tests)
            setattr(loaded_testcase, "runner", test_runner)
            test_suite.addTest(loaded_testcase)

        return test_suite
