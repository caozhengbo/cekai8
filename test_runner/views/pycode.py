from django.http import JsonResponse
import json
from test_runner import models
from test_runner.utils.runner import DebugCode


def pycode1(request):
    if request.method == "GET":
        # <QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'project': ['13'], 'search': ['']}>
        project = request.GET.get("project")
        search = request.GET.get("search")
        pys = models.PycodeModel.objects.filter(project_id=project)
        if search:
            pys = pys.filter(name__contains=search)
        pys = pys.values()
        data = {
            "count": len(pys),
            "results": list(pys)
        }
        return JsonResponse(data)
    elif request.method == "POST":
        reqObj = json.loads(request.body.decode('utf-8'))
        # {'name': 'test001', 'desc': 'test', 'project': '13', 'id': ''}
        name = reqObj.get("name")
        desc = reqObj.get("desc")
        project = models.ProjectMode.objects.get(pk=reqObj.get("project"))
        id = reqObj.get("id")

        models.PycodeModel.objects.create(name=name,
                                          desc=desc,
                                          project=project)
        return JsonResponse({"success": True})

    elif request.method == "DELETE":
        pass


def pycode2(request, pk):
    if request.method == "GET":
        pys = models.PycodeModel.objects.get(pk=pk)
        data = {
            "code": pys.code,
            "id": pys.id,
        }
        return JsonResponse(data)

    elif request.method == "PATCH":
        reqObj = json.loads(request.body.decode('utf-8'))
        # {'code': '# _*_ coding:utf-8 _*_', 'id': 1}
        code = reqObj.get("code")
        id = reqObj.get("id")

        pys = models.PycodeModel.objects.get(pk=id)
        pys.code = code
        pys.save()
        return JsonResponse({"success": True})


def runpycode(request, pk):
    if request.method == "GET":
        # <QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'project': ['13']}>   pk=id
        # print(request.GET)
        # print(pk)  # 1
        pys = models.PycodeModel.objects.get(pk=pk)

        # 代码、项目ID、代码名称
        debug = DebugCode(pys.code, request.GET.get("project"), pys.name)
        debug.run()
        print(debug.resp)
        data = {
            "msg": debug.resp
        }
        return JsonResponse(data)
