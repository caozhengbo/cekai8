import datetime
import importlib
import shutil
import types

import requests
import yaml
from httprunner import HttpRunner
from requests.cookies import RequestsCookieJar

from test_runner.utils import responseData
import tempfile
import os
from cekai8.settings import BASE_DIR
import io
import json
import sys
from bs4 import BeautifulSoup
from test_runner.models import VariableModel, PycodeModel, ReportModel, ReportDetailModel, DebugtalkModel, \
    ModelWithFileFieldModel
from test_runner.models import ProjectMode as ProjectModel


def parse_tests(testcases, debugtalk, project, name=None, config=None):
    """get test case structure
        testcases: list
        config: none or dict
        debugtalk: dict
    """
    refs = {
        "env": {},
        "def-api": {},
        "def-testcase": {},
        "debugtalk": debugtalk
    }
    testset = {
        "config": {
            "name": testcases[-1]["name"],
            "variables": []
        },
        "teststeps": testcases,
    }

    if config:
        if "parameters" in config.keys():
            for content in config["parameters"]:
                for key, value in content.items():
                    try:
                        content[key] = eval(value.replace("\n", ""))
                    except:
                        content[key] = value
        if 'outParams' in config.keys():
            config["output"] = []
            out_params = config.pop('outParams')
            for params in out_params:
                config["output"].append(params["key"])
        testset["config"] = config

    if name:
        testset["config"]["name"] = name

    global_variables = []

    for variables in VariableModel.objects.filter(project__id=project).values("key", "value"):
        if testset["config"].get("variables"):
            for content in testset["config"]["variables"]:
                if variables["key"] not in content.keys():
                    global_variables.append({variables["key"]: variables["value"]})
        else:
            global_variables.append({variables["key"]: variables["value"]})

    if not testset["config"].get("variables"):
        testset["config"]["variables"] = global_variables
    else:
        testset["config"]["variables"].extend(global_variables)

    testset["config"]["refs"] = refs

    return testset


def parse_summary(summary):
    """序列化summary
    """
    for detail in summary["details"]:

        for record in detail["records"]:

            for key, value in record["meta_data"]["request"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["request"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["request"][key] = requests.utils.dict_from_cookiejar(value)

            for key, value in record["meta_data"]["response"].items():
                if isinstance(value, bytes):
                    record["meta_data"]["response"][key] = value.decode("utf-8")
                if isinstance(value, RequestsCookieJar):
                    record["meta_data"]["response"][key] = requests.utils.dict_from_cookiejar(value)

            if "text/html" in record["meta_data"]["response"]["content_type"]:
                record["meta_data"]["response"]["content"] = \
                    BeautifulSoup(record["meta_data"]["response"]["content"], features="html.parser").prettify()

    return summary


def is_function(tup):
    """ Takes (name, object) tuple, returns True if it is a function.
    """
    name, item = tup
    return isinstance(item, types.FunctionType)


def is_variable(tup):
    """ Takes (name, object) tuple, returns True if it is a variable.
    """
    name, item = tup
    if callable(item):
        # function or class
        return False
    if isinstance(item, types.ModuleType):
        # imported module
        return False
    if name.startswith("_"):
        # private property
        return False

    return True


class FileLoader(object):

    @staticmethod
    def dump_yaml_file(yaml_file, data):
        """ dump yaml file
        """
        with io.open(yaml_file, 'w', encoding='utf-8') as stream:
            yaml.dump(data, stream, indent=4, default_flow_style=False, encoding='utf-8', allow_unicode=True)

    @staticmethod
    def dump_json_file(json_file, data):
        """ dump json file
        """
        with io.open(json_file, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, indent=4, separators=(',', ': '), ensure_ascii=False)

    @staticmethod
    def dump_python_file(python_file, data):
        """dump python file
        """
        with io.open(python_file, 'w', encoding='utf-8') as stream:
            stream.write(data)

    @staticmethod
    def dump_binary_file(binary_file, data):
        """dump file
        """
        with io.open(binary_file, 'wb') as stream:
            stream.write(data)

    @staticmethod
    def copy_file(path, to_path):
        """
        copy file to_path
        """
        shutil.copyfile(path, to_path)

    @staticmethod
    def load_python_module(file_path):
        """ load python module.

        Args:
            file_path: python path

        Returns:
            dict: variables and functions mapping for specified python module

                {
                    "variables": {},
                    "functions": {}
                }

        """
        debugtalk_module = {
            "variables": {},
            "functions": {}
        }

        sys.path.insert(0, file_path)
        module = importlib.import_module("debugtalk")
        # 修复重载bug
        importlib.reload(module)
        sys.path.pop(0)

        for name, item in vars(module).items():
            if is_function((name, item)):
                debugtalk_module["functions"][name] = item
            elif is_variable((name, item)):
                if isinstance(item, tuple):
                    continue
                debugtalk_module["variables"][name] = item
            else:
                pass

        return debugtalk_module


def load_debugtalk(project):
    """import debugtalk.py in sys.path and reload
        project: int
    """
    tempfile_path = tempfile.mkdtemp(prefix='tempHttpRunner', dir=os.path.join(BASE_DIR, 'tempWorkDir'))
    debugtalk_path = os.path.join(tempfile_path, 'debugtalk.py')

    os.chdir(tempfile_path)
    try:
        py_files = PycodeModel.objects.filter(project__id=project)
        if py_files:
            for file in py_files:
                # file_path = os.path.join(tempfile_path, file.name)
                FileLoader.dump_python_file(debugtalk_path, file.code)
                FileLoader.load_python_module(os.path.dirname(debugtalk_path))
        else:
            code = DebugtalkModel.objects.get(project=project)
            FileLoader.dump_python_file(debugtalk_path, code.code)
        testdata_files = ModelWithFileFieldModel.objects.filter(project__id=project)
        for testdata in testdata_files:
            testdata_path = os.path.join(tempfile_path, testdata.name)
            myfile_path = os.path.join(BASE_DIR, 'media', str(testdata.file))
            FileLoader.copy_file(myfile_path, testdata_path)
        debugtalk = FileLoader.load_python_module(os.path.dirname(debugtalk_path))

        return debugtalk, debugtalk_path
    except Exception as e:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))
        raise SyntaxError(str(e))


def debug_api(api, project, name=None, config=None, save=False, test_data=None, report_name=''):
    """debug api
        api :dict or list
        project: int
    """
    if len(api) == 0:
        return responseData.TEST_NOT_EXISTS

    # testcases
    if isinstance(api, dict):
        """
        httprunner scripts or teststeps
        """
        api = [api]

    debugtalk = load_debugtalk(project)

    debugtalk_content = debugtalk[0]
    debugtalk_path = debugtalk[1]

    os.chdir(os.path.dirname(debugtalk_path))
    try:
        testcase_list = [parse_tests(api, debugtalk_content, project, name=name, config=config)]

        fail_fast = False
        if config and 'failFast' in config.keys():
            fail_fast = True if (config["failFast"] == 'true' or config["failFast"] == True) else False

        kwargs = {
            "failfast": fail_fast
        }
        if test_data != None:
            os.environ["excelName"] = test_data[0]
            os.environ["excelsheet"] = test_data[1]

        # print("kwargs:", kwargs)
        runner = HttpRunner(**kwargs)
        # HttpRunner
        runner.run(testcase_list)

        summary = parse_summary(runner.summary)
        if save:
            save_summary(report_name, summary, project, type=1)
        return summary
    except Exception as e:
        # print("---------------",e)
        if e:
            raise SyntaxError(str(e))
        else:
            return
    finally:
        os.chdir(BASE_DIR)
        shutil.rmtree(os.path.dirname(debugtalk_path))


def save_summary(name, summary, project, type=2):
    """保存报告信息
    """
    if "status" in summary.keys():
        return
    if name == "":
        name = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    simple_summary = {
        "time": summary["time"],
        "platform": summary["platform"],
        "stat": summary["stat"],
        "success": summary["success"],
    }
    project_class = ProjectModel.objects.get(id=project)
    report = ReportModel.objects.create(**{
        "project": project_class,
        "name": name,
        "type": type,
        "summary": json.dumps(simple_summary)
    })
    report.save()
    report_detail = ReportDetailModel.objects.create(**{
        "project": project_class,
        "name": name,
        "report": report,
        "summary": json.dumps(summary, ensure_ascii=False)
    })
    report_detail.save()
