# -*- coding: utf-8 -*-

"""httprunner较低层接口，用于执行测试用例
"""

import os
import unittest
import pprint

from sentry_sdk import capture_message

from httprunner import (__version__, exceptions, loader, logger, parser,
                        report, runner, utils)


class HttpRunner(object):
    """ Developer Interface: Main Interface
        Usage:

            from httprunner.api import HttpRunner
            runner = HttpRunner(
                failfast=True,
                save_tests=True,
                log_level="INFO",
                log_file="test.log"
            )
            summary = runner.run(path_or_tests)

    """

    def __init__(self, failfast=False, save_tests=False, log_level="INFO", log_file=None):
        """ initialize HttpRunner.

        Args:
            failfast (bool): stop the test run on the first error or failure.
            save_tests (bool): save loaded/parsed test_case to JSON file.
            log_level (str): logging level.
            log_file (str): log file path.

        """
        logger.setup_logger(log_level, log_file)

        self.exception_stage = "initialize HttpRunner()"
        kwargs = {
            "failfast": failfast,
            "resultclass": report.HtmlTestResult
        }
        self.unittest_runner = unittest.TextTestRunner(**kwargs)
        self.test_loader = unittest.TestLoader()
        self.save_tests = save_tests
        self._summary = None
        self.project_working_directory = None

    def _add_tests(self, testcases):
        """ initialize test_case with Runner() and add to test suite.

        Args:
            testcases (list): testcases list.

        Returns:
            unittest.TestSuite()

        """
        def _add_test(test_runner, test_dict):
            """ add test to test_case.
            """

            def test(self):
                try:
                    test_runner.run_test(test_dict)
                except exceptions.MyBaseFailure as ex:
                    self.fail(str(ex))
                finally:
                    self.meta_datas = test_runner.meta_datas

            if "config" in test_dict:
                # run nested test_case
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
            test_runner = runner.Runner(config)
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
                    # suppose one test_case should not have more than 9999 steps,
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

    def _run_suite(self, test_suite):
        """ run test_case in test_suite

        Args:
            test_suite: unittest.TestSuite()

        Returns:
            list: tests_results

        """
        tests_results = []

        for testcase in test_suite:
            testcase_name = testcase.config.get("name")
            logger.log_info("Start to run test_case: {}".format(testcase_name))

            result = self.unittest_runner.run(testcase)
            if result.wasSuccessful():
                tests_results.append((testcase, result))
            else:
                tests_results.insert(0, (testcase, result))

        return tests_results

    def _aggregate(self, testcases_results, testcase_details=None):
        """ aggregate results

        Args:
            testcases_results (list): list of (test_case, result)

        """
        summary = {
            "success": True,
            "stat": {
                "testcases": {
                    "total": len(testcases_results),
                    "success": 0,
                    "fail": 0
                },
                "teststeps": {}
            },
            "time": {},
            "platform": report.get_platform(),
            "details": []
        }

        # custom
        for index_case, tests_result in enumerate(testcases_results):
            testcase, result = tests_result
            testcase_summary = report.get_summary(result)

            if testcase_summary["success"]:
                summary["stat"]["testcases"]["success"] += 1
            else:
                summary["stat"]["testcases"]["fail"] += 1

            summary["success"] &= testcase_summary["success"]
            testcase_summary["name"] = testcase.config.get("name")
            testcase_summary["in_out"] = utils.get_testcase_io(testcase)

            report.aggregate_stat(
                summary["stat"]["teststeps"], testcase_summary["stat"])
            report.aggregate_stat(summary["time"], testcase_summary["time"])

            # ==================================================
            # custom: add step detail to summary, by zheng.zhang
            # step detail path in summary: summary.details[i].records[j].step_detail
            teststeps = testcase.teststeps
            for index_step, teststep in enumerate(teststeps):
                try:
                    step_detail = parser.parse_variables_mapping(teststep["variables"])
                    testcase_summary["records"][index_step]["step_detail"] = step_detail
                except exceptions.VariableNotFound as e:
                    # TODO: deal with various built-in Exception
                    testcase_summary["records"][index_step]["step_detail"] = {
                        "internel error message": \
                            "error during adding step details: VariableNotFound",
                        "Exception message": e
                    }
                    # print("error during adding step detail to summary,  \
                    #     in {}".format(__file__))
            
            # ==================================================

            summary["details"].append(testcase_summary)

        return summary

    def run_tests(self, tests_mapping):
        """ run test_case/testsuite data
        """
        capture_message("start to run test_case")
        project_mapping = tests_mapping.get("project_mapping", {})
        self.project_working_directory = project_mapping.get(
            "PWD", os.getcwd())

        if self.save_tests:
            utils.dump_logs(tests_mapping, project_mapping, "loaded")

        # parse test_case
        self.exception_stage = "parse test_case"
        parsed_testcases = parser.parse_tests(tests_mapping)
        parse_failed_testfiles = parser.get_parse_failed_testfiles()
        if parse_failed_testfiles:
            logger.log_warning("parse failures occurred ...")
            utils.dump_logs(parse_failed_testfiles, project_mapping, "parse_failed")

        if self.save_tests:
            utils.dump_logs(parsed_testcases, project_mapping, "parsed")

        # add test_case to test suite
        self.exception_stage = "add test_case to test suite"
        test_suite = self._add_tests(parsed_testcases)

        # run test suite
        self.exception_stage = "run test suite"
        testcases_results = self._run_suite(test_suite)

        # aggregate results
        self.exception_stage = "aggregate results"
        testcase_details = tests_mapping.get("testcases", [])
        self._summary = self._aggregate(testcases_results, testcase_details)

        # generate html report
        self.exception_stage = "generate html report"
        report.stringify_summary(self._summary)

        if self.save_tests:
            utils.dump_logs(self._summary, project_mapping, "summary")

        return self._summary

    def get_vars_out(self):
        """ get variables and output
        Returns:
            list: list of variables and output.
                if test_case are parameterized, list items are corresponded to parameters.

                [
                    {
                        "in": {
                            "user1": "leo"
                        },
                        "out": {
                            "out1": "out_value_1"
                        }
                    },
                    {...}
                ]

            None: returns None if test_case not started or finished or corrupted.

        """
        if not self._summary:
            return None

        return [
            summary["in_out"]
            for summary in self._summary["details"]
        ]

    def run_path(self, path, dot_env_path=None, mapping=None):
        """ run test_case/testsuite file or folder.

        Args:
            path (str): test_case/testsuite file/foler path.
            dot_env_path (str): specified .env file path.
            mapping (dict): if mapping is specified, it will override variables in config block.

        Returns:
            dict: result summary

        """
        # load test_case
        self.exception_stage = "load test_case"
        tests_mapping = loader.load_cases(path, dot_env_path)

        if mapping:
            tests_mapping["project_mapping"]["variables"] = mapping

        return self.run_tests(tests_mapping)

    def run(self, path_or_tests, dot_env_path=None, mapping=None):
        """ main interface.

        Args:
            path_or_tests:
                str: test_case/testsuite file/foler path
                dict: valid test_case/testsuite data
            dot_env_path (str): specified .env file path.
            mapping (dict): if mapping is specified, it will override variables in config block.

        Returns:
            dict: result summary

        """
        logger.log_info("HttpRunner version: {}".format(__version__))
        if loader.is_test_path(path_or_tests):
            return self.run_path(path_or_tests, dot_env_path, mapping)
        elif loader.is_test_content(path_or_tests):
            project_working_directory = path_or_tests.get("project_mapping", {}).get("PWD", os.getcwd())
            loader.init_pwd(project_working_directory)
            return self.run_tests(path_or_tests)
        else:
            print(path_or_tests)
            raise exceptions.ParamsError(
                "Invalid test_case path or testcases: {}".format(path_or_tests))
