from test_runner.models import VariableModel, ProjectMode
from django.http import JsonResponse
import json
from test_runner.utils import responseData


def variables(request):
    if request.method == "GET":
        # <QueryDict: {'token': ['e3ec1a7fb7aa7c5f000aeb2ae6cff64d'], 'project': ['7'], 'search': ['']}>
        project = request.GET.get("project")
        search = request.GET.get('search')
        vars = VariableModel.objects.all().filter(project=project)

        if search != "":  # 这里用来判断筛选的  __contains（包含）
            vars = vars.filter(key__contains=search)
        vars = vars.values()
        data = {
            "success": True,
            "results": list(vars)
        }
        return JsonResponse(data)


    elif request.method == "POST":
        reqObj = json.loads(request.body.decode('utf-8'))
        # {'key': 'var', 'value': 'ces', 'desc': '123', 'project': '7'}
        key = reqObj['key']
        value = reqObj['value']
        desc = reqObj['desc']
        project = ProjectMode.objects.get(pk=reqObj['project'])

        try:
            VariableModel.objects.filter(project=project.id).get(key=key)
            # 说明已经给该项目添加过这个变量了
            return JsonResponse(responseData.VARIABLE_EXIST)
        except VariableModel.DoesNotExist as e:
            # 该变量可以创建
            VariableModel.objects.create(key=key, value=value, desc=desc, project=project)
            data = {
                "success": True,
                "msg": "配置新增成功"
            }
            return JsonResponse(data)

    elif request.method == "DELETE":  # delAllVariabels
        reqObj = json.loads(request.body.decode('utf-8'))
        """
        [{'id': 1, 'create_time': '2021-12-12T16:12:21.501Z', 'update_time': '2021-12-12T16:12:21.502Z', 'key': 'vars', 'value': 'qwer', 'desc': 'ceshicehsi', 'project_id': 7}, {'id': 2, 'create_time': '2021-12-12T16:14:00.897Z', 'update_time': '2021-12-12T16:14:00.897Z', 'key': 'vars2', 'value': '123', 'desc': '213', 'project_id': 7}]
        """


def variables1(request, pk):
    if request.method == "PATCH":
        reqObj = json.loads(request.body.decode('utf-8'))  # 这里前端没有传projectID
        # {'key': 'vars', 'value': 'qwer', 'desc': 'ceshicehsi', 'id': 1}
        key = reqObj['key']
        value = reqObj['value']
        desc = reqObj['desc']
        id = reqObj['id']

        try:
            v = VariableModel.objects.get(pk=id)
            # print(v.project.name) # 知识点：这样可以拿到对应主键的内容
            # 在当前项目的所有变量中 判断新的名字是否有冲突
            if key != v.key:
                vars = VariableModel.objects.filter(project=v.project.id)  # 当前变量所对应的项目的所有变量
                try:
                    vars.get(key=key)
                    # 说明名称在当前项目是存在的，无法创建
                    data = {
                        "success": False,
                        "msg": "变量名已存在"
                    }
                    return JsonResponse(data)
                except VariableModel.DoesNotExist as e:
                    v.key = key
                    v.value = value
                    v.desc = desc
                    v.save()
                    data = {
                        "success": True,
                        "msg": "变量修改成功"
                    }
                    return JsonResponse(data)
            else:
                # v.key = key  说明变量名没有做修改 就不需要赋值了
                v.value = value
                v.desc = desc
                v.save()
                data = {
                    "success": True,
                    "msg": "变量修改成功"
                }
                return JsonResponse(data)

        except VariableModel.DoesNotExist as e:
            # 变量已经找不到了
            data = {
                "success": False,
                "msg": "变量不存在"
            }
            return JsonResponse(data)



    elif request.method == "DELETE":
        # reqObj = request.GET  没传值 需要用pk进行处理
        # r<QueryDict: {'token': ['e3ec1a7fb7aa7c5f000aeb2ae6cff64d']}>
        try:
            v = VariableModel.objects.get(pk=pk)
            v.delete()
            data = {
                "success": True,
                "msg": "删除成功"
            }
            return JsonResponse(data)
        except VariableModel.DoesNotExist as e:
            data = {
                "success": False,
                "msg": "变量不存在"
            }
            return JsonResponse(data)
