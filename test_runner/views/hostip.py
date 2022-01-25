from test_runner.models import HostIPModel, ProjectMode
import json
from django.http import JsonResponse


def host(request):
    if request.method == "GET":
        # <QueryDict: {'token': ['b33141357eeccc4c90d3291844b11b09'], 'project': ['7']}>
        project = request.GET.get('project')
        hosts = HostIPModel.objects.all().filter(project=project).values()
        count = HostIPModel.objects.all().filter(project=project).count()
        data = {
            "success": True,
            "count": count,
            "results": list(hosts)
        }
        return JsonResponse(data)
    elif request.method == "POST":
        reqObj = json.loads(request.body.decode('utf-8'))
        # {'name': 'host', 'value': '127.0.0.1 localhost\n127.0.0.2 localhost', 'project': '7'}
        name = reqObj["name"]
        value = reqObj["value"]
        project = ProjectMode.objects.get(pk=reqObj['project'])
        try:
            # 判断下name是否存在
            HostIPModel.objects.filter(project=reqObj['project']).get(name=name)
            data = {
                "success": False,
                "msg": "环境名已存在"
            }
            return JsonResponse(data)
        except HostIPModel.DoesNotExist as e:
            HostIPModel.objects.create(name=name, value=value, project=project)
            data = {
                "success": True,
            }
            return JsonResponse(data)


def host1(request, pk):
    if request.method == "GET":
        # 获取当前项目的所有环境
        try:
            hosts = HostIPModel.objects.filter(project=pk).values()
            data = {
                "success": True,
                "results": list(hosts)
            }
            return JsonResponse(data)

        except HostIPModel.DoesNotExist as e:
            pass
    elif request.method == "PATCH":
        reqObj = json.loads(request.body.decode("utf-8"))
        # {'name': '测试', 'value': '测试1', 'id': 1}
        name = reqObj["name"]
        value = reqObj["value"]
        id = reqObj["id"]
        try:
            h = HostIPModel.objects.get(pk=id)  # 找到当前修改的原信息
            if h.name != name:  # 如果走到这里 说明name这次有修改
                hosts = HostIPModel.objects.filter(project=h.project.id)  # 可以获取到说明新的name在数据库中已经存在
                try:
                    hosts.get(name=name)  # 如果在当前项目可以找到相同的name，就return
                    data = {
                        "success": False,
                        "msg": "在当前项目中，环境名已存在"
                    }
                    return JsonResponse(data)
                except HostIPModel.DoesNotExist as e:  # 说明没有找到已存在name的值，可以进行修改
                    h.name = name
                    h.value = value
                    h.save()
                    data = {
                        "success": True,
                        "msg": "修改成功"
                    }
                    return JsonResponse(data)
            else:  # 否则name本次没有做修改  只是修改了value
                h.value = value
                h.save()
                data = {
                    "success": True,
                    "msg": "修改成功"
                }
                return JsonResponse(data)
        except HostIPModel.DoesNotExist as e:  # 没有找到项目，说明已经被别人删除了
            data = {
                "success": False,
                "msg": "项目已被删除"
            }
            return JsonResponse(data)


    elif request.method == "DELETE":
        # reqObj = json.loads(request.body.decode('utf-8'))
        # <QueryDict: {'token': ['b33141357eeccc4c90d3291844b11b09']}>

        try:
            h = HostIPModel.objects.get(pk=pk)
            h.delete()
            data = {
                "success": True,
                "msg": "删除成功"
            }
            return JsonResponse(data)
        except HostIPModel.DoesNotExist as e:
            data = {
                "success": False,
                "msg": "环境不存在"
            }
            return JsonResponse(data)
