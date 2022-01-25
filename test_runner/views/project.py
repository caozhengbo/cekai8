import json

from test_runner.models import ProjectMode, VariableModel, HostIPModel, ConfigModel, RelationModel,ApiModel,CaseModel
from django.http import JsonResponse


def project1(request):
    # 获取当前登录用户的所有项目
    if request.method == "GET":
        pros = ProjectMode.objects.all().filter().values()
        data = {
            "success": True,
            "results": list(pros)
        }
        return JsonResponse(data)
    elif request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))  # {"name":"123","desc":"123","id":""}
        name = req['name']
        desc = req['desc']
        responsible = req['responsible']

        # 验证项目是否存在
        try:
            ProjectMode.objects.get(name=req['name'])
            # 项目已存在
            data = {
                "success": False,
                "msg": "该项目已存在"
            }
            return JsonResponse(data)

        except ProjectMode.DoesNotExist as e:
            # 项目不存在
            p = ProjectMode.objects.create(name=name, desc=desc, responsible=responsible)
            # 对项目进行一些初始化操作，创建一个API的数结构 tree
            RelationModel.objects.create(project=p, type=1)
            # 创建一个测试用例的树结构
            RelationModel.objects.create(project=p, type=2)
            data = {
                "success": True,
                "msg": "项目创建成功"
            }
            return JsonResponse(data)
    elif request.method == "PATCH":
        # 修改当前登录的用户的某个项目
        reqObj = json.loads(request.body.decode('utf-8'))
        # print(reqObj)
        # {'name': 'aaaaa1', 'desc': '123', 'responsible': 'admin', 'id': 4}
        id = reqObj['id']
        name = reqObj['name']
        desc = reqObj['desc']
        responsible = reqObj['responsible']

        try:
            pObj = ProjectMode.objects.get(pk=id)
            # 在修改之前验证下新名字是否可用
            if name != pObj.name:  # name这次修改是有改动的
                try:
                    tmpObj = ProjectMode.objects.get(name=name)  # 如果get能获取到这次修改的名字，说明name已经在数据库存在了
                    date = {
                        "success": False,
                        "msg": "项目已经存在"
                    }
                    return JsonResponse(date)
                except ProjectMode.DoesNotExist as e:
                    # 走到这里说明 没有在数据库查询到已存在的name，可以对这次修改的内容进行赋值并保存
                    pObj.name = name
                    pObj.desc = desc
                    pObj.responsible = responsible
                    pObj.save()
                    data = {
                        "success": True,
                        "msg": "项目修改成功"
                    }
                    return JsonResponse(data)
            else:
                # 这次name没有改动
                pObj.desc = desc
                pObj.responsible = responsible
                pObj.save()
                data = {
                    "success": True,
                    "msg": "项目修改成功"
                }
                return JsonResponse(data)

        except ProjectMode.DoesNotExist as e:
            # 在修改之前已经找不到这个项目了
            data = {
                "success": False,
                "msg": "项目不存在"
            }
            return JsonResponse(data)

    elif request.method == "DELETE":
        reqObj = json.loads(request.body.decode('utf-8'))
        # {'id': 4}
        try:
            pObj = ProjectMode.objects.get(pk=reqObj['id'])
            """
            判断是否有正在运行的测试用例，如果有则不删除项目
            注意：还要删除该项目相关的变量、环境、api、测试用例
            # VariableModel, HostIPModel, ConfigModel, RelationModel
            """
            VariableModel.objects.filter(project=pObj.id).delete()
            HostIPModel.objects.filter(project=pObj.id).delete()
            ConfigModel.objects.filter(project=pObj.id).delete()
            RelationModel.objects.filter(project=pObj.id).delete()

            pObj.delete()
            data = {
                "success": True,
                "msg": ""
            }
            return JsonResponse(data)
        except ProjectMode.DoesNotExist as e:
            data = {
                "success": False,
                "msg": "项目不存在"
            }
            return JsonResponse(data)


def project2(request, pk):
    if request.method == "GET":
        # 获取当前登录用户的某个项目的详细详细
        try:
            p = ProjectMode.objects.get(pk=pk)
            # [resp.successes,resp.failure,resp.error,resp.skippe]
            data = {
                "success": True,
                "name": p.name,
                "desc": p.desc,
                "api_count": ApiModel.objects.filter(project=pk).count(),
                "case_count": CaseModel.objects.filter(project=pk).count(),
                "config_count": ConfigModel.objects.filter(project=pk).count(),
                "variables_count": VariableModel.objects.filter(project=pk).count(),
                "host_count": HostIPModel.objects.filter(project=pk).count(),
                "task_count": 0,
                "report_count": 0,
                "uitestplan": 0,
            }
            return JsonResponse(data)
        except ProjectMode.DoesNotExist:
            data = {
                "success": False,
                "msg": "该项目已被删除"
            }
            return JsonResponse(data)


def gettagcount(request):
    if request.method == "GET":
        # {'token': ['ffe33bfc2d5203221a4c647ef7788782'], 'project': ['2']}
        # 待补充业务逻辑，找到这个项目的所有测试用例，看每种类型用例各有多少个
        data = {
            "typename": ["冒烟", "集成", "测试"],
            "countlist": [5, 6, 3]
        }
        return JsonResponse(data)


def getreporttail(request):
    if request.method == "GET":
        # {'token': ['ffe33bfc2d5203221a4c647ef7788782'], 'project': ['2']}
        # 待补充业务逻辑，找到这个项目的所有测试用例，看运行情况的数量
        data = {
            "successes": 5,
            "failure": 4,
            "error": 1,
            "skippe": 1,
        }
        return JsonResponse(data)
