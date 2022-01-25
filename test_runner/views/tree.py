from test_runner.models import RelationModel
import json
import pprint
from django.http import JsonResponse


def tree1(request, pk):
    if request.method == "GET":
        # < QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'type': ['1']} >
        # 13
        # rm = RelationModel.objects.filter(project_id=pk, type=request.GET.get("type"))
        print(request.GET.get("type"),"___________GT")
        print(pk)
        tree_type = request.GET.get("type")
        rm = RelationModel.objects.filter(project_id=pk).get(type=tree_type)
        # body = eval(rm.tree)
        body = eval(rm.tree)
        data = {
            "tree": body,
            "id": rm.id,
            # "max": ""
        }
        return JsonResponse(data)


    elif request.method == "PATCH":
        reqObj = json.loads(request.body.decode('utf-8'))
        """
        {'body': [{'children': [],
           'id': 'f20ad9ac-fc0b-e637-8530-1448505f6a03',
           'label': '123'}],
             'mode': False,
             'type': 1}
        """
        body = reqObj.get("body")
        mode = reqObj.get("mode")

        rm = RelationModel.objects.get(pk=pk)
        rm.tree = body
        rm.save()
        if mode:
            # 删除该节点下的所有的API
            pass

        data = {
            "tree": body,
            "success": True
        }
        return JsonResponse(data)


# 单例模式
# class A(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super.__new__(cls, *args, **kwargs)
#         return cls._instance
