import json

from test_runner import models
from django.http import JsonResponse
from jsonpath import jsonpath


def generate_casestep(body, case, pk):
    pass


def test1(request):
    if request.method == "GET":
        # <QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'project': ['13'], 'node': [''], 'search': [''], 'tag': ['']}>
        project = request.GET.get("project")
        node = request.GET.get("node")
        search = request.GET.get("search")
        tag = request.GET.get("tag")
        testcase = models.CaseModel.objects.filter(project_id=project).order_by("-update_time")
        if node:
            testcase = testcase.filter(relation=node)
        if tag:
            testcase = testcase.filter(tag=tag)
        if search:
            testcase = testcase.filter(name__contains=search)
        testcase = testcase.values()
        data = {
            "count": len(testcase),
            "results": list(testcase)
        }
        return JsonResponse(data)
    elif request.method == "POST":
        reqObj = json.loads(request.body.decode('utf8'))

        length = reqObj.get("length")
        project = reqObj.get("project")
        relation = reqObj.get("relation")
        name = reqObj.get("name")
        body = reqObj.get("body")
        tag = reqObj.get("tag")

        tag_options = {
            "冒烟用例": 1,
            "集成用例": 2,
            "监控脚本": 3,
            "回归用例": 4,
            "系统用例": 5,
            "空库用例": 6
        }

        case = models.CaseModel.objects.create(name=name,
                                               relation=relation,
                                               length=length,
                                               tag=tag_options.get(tag),
                                               project_id=project)
        # 创建测试用例步骤，一个API对应一个步骤
        generate_casestep(body, case, project)
        return JsonResponse({"success": True})

    elif request.method == "DELETE":
        pass


def test2(request, pk):
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass
    elif request.method == "DELETE":
        pass
    elif request.method == "PATCH":
        pass
