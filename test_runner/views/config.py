from test_runner.models import ConfigModel, ProjectMode
from django.http import JsonResponse
import json
from test_runner.utils import parser
import pprint


def config(request):
    if request.method == "GET":
        # reqObj = request.GET
        #  <QueryDict: {'token': ['b33141357eeccc4c90d3291844b11b09'], 'project': ['7'], 'search': ['']}>
        project = request.GET.get('project')
        search = request.GET.get('search')
        cons = ConfigModel.objects.filter(project=project).values()
        count = ConfigModel.objects.filter(project=project).count()

        data = {
            "success": True,
            "results": list(cons),
            "count": count
        }
        return JsonResponse(data)
    elif request.method == "POST":
        reqObj = json.loads(request.body.decode("utf-8"))
        """
        {'parameters': {'parameters': [], 'desc': {}},
         'header': {'header': {}, 'desc': {}},
         'request': {'form': {'data': {}, 'desc': {}},
                     'json': {},
                     'params': {'params': {}, 'desc': {}},
                     'files': {'files': {}, 'desc': {}}},
         'variables': {'variables': [{'name': '1'}, {'key': 2}],
                       'desc': {'name': 'nameTest', 'key': 'keyTest'}},
         'hooks': {'setup_hooks': [], 'teardown_hooks': []},
         'base_url': 'http://www.baidu.com',
         'configdesc': 'test',
         'name': '123',
         'project': '7'}
        """
        name = reqObj["name"]
        base_url = reqObj["name"]
        try:
            configdesc = reqObj['configdesc']
        except KeyError as e:
            configdesc = None

        project = ProjectMode.objects.get(pk=reqObj['project'])
        configObj = parser.Format(body=reqObj, level='config')
        configObj.parse()
        """  configObj.testcase: 这是解析后的内容
        {'name': '123',
         'request': {'base_url': 'http://www.baidu.com'},
         'desc': {'header': {},
                  'data': {},
                  'files': {},
                  'params': {},
                  'variables': {'name': 'nameTest', 'key': 'keyTest'},
                  'parameters': {}},
         'variables': [{'name': '1'}, {'key': 2}]}
        """

        # 验证新创建的name在数据库中是否存在
        cons = ConfigModel.objects.filter(project=project)
        try:
            cons.get(name=name)  # 如果在当前项目中已经存在这个名字了，就不允许创建了
            data = {
                "success": False,
                "msg": "配置名称重复"
            }
            return JsonResponse(data)
        except ConfigModel.DoesNotExist as e:
            # 能走到这里说明在库里没有找到
            ConfigModel.objects.create(name=name,
                                       body=configObj.testcase,
                                       base_url=base_url,
                                       configdesc=configdesc,
                                       project=project)

            data = {
                "success": True,
                "msg": ""
            }
            return JsonResponse(data)
    elif request.method == "DELETE":
        reqObj = json.loads(request.body.decode("utf-8"))
        # print(type(reqObj))
        """
        [{'id': 1,
          'create_time': '2021-12-14T16:05:56.465Z',
          'update_time': '2021-12-14T16:05:56.465Z',
          'name': '123',
          'body': "{'name': '123', 'request': {'base_url': 'http://www.baidu.com'}, "
                  "'desc': {'header': {}, 'data': {}, 'files': {}, 'params': {}, "
                  "'variables': {'name': 'nameTest', 'key': 'keyTest'}, 'parameters': "
                  "{}}, 'variables': [{'name': '1'}, {'key': 2}]}",
          'base_url': '123',
          'configdesc': 'test',
          'project_id': 7},
         {'id': 2,
          'create_time': '2021-12-14T16:09:58.714Z',
          'update_time': '2021-12-14T16:09:58.714Z',
          'name': '1231',
          'body': "{'name': '1231', 'request': {'base_url': '123'}, 'desc': {'header': "
                  "{}, 'data': {}, 'files': {}, 'params': {}, 'variables': {'123': "
                  "''}, 'parameters': {}}, 'variables': [{'123': '123'}]}",
          'base_url': '1231',
          'configdesc': '123',
          'project_id': 7}]
        """
        for cDict in reqObj:
            try:
                # 删除前判断下配置是否存在
                ConfigModel.objects.get(pk=cDict['id']).delete()
            except ConfigModel.DoesNotExist as e:
                # data = {
                #     "success": False,
                #     "msg": "内容不存在"
                # }
                # return JsonResponse(data)
                pass
        data = {
            "success": True,
            "msg": ""
        }
        return JsonResponse(data)


def config1(request, pk):
    if request.method == "GET":
        cons = ConfigModel.objects.filter(project=pk).values()
        data = {
            "success": True,
            "results": list(cons),
        }
        return JsonResponse(data)

    elif request.method == "POST":  # copyConfig
        reqObj = json.loads(request.body.decode("utf-8"))
        # {'name': '321'}
        name = reqObj['name']
        try:
            # 判断一下新的name是否存在
            ConfigModel.objects.get(name=name)
            data = {
                "success": False,
                "msg": "配置名称已存在"
            }
            return JsonResponse(data)
        except ConfigModel.DoesNotExist as e:
            try:
                cons = ConfigModel.objects.get(pk=pk)
                ConfigModel.objects.create(name=name,
                                           body=cons.body,
                                           base_url=cons.base_url,
                                           configdesc=cons.configdesc,
                                           project=ProjectMode.objects.get(pk=cons.project.id))
                data = {
                    "success": True,
                    "msg": ""
                }
                return JsonResponse(data)
            except ConfigModel.DoesNotExist as e:
                data = {
                    "success": False,
                    "msg": "配置信息已被删除"
                }
                return JsonResponse(data)
    elif request.method == "DELETE":
        try:
            ConfigModel.objects.get(pk=pk).delete()
            data = {
                "success": True,
                "msg": ""
            }
            return JsonResponse(data)
        except ConfigModel.DoesNotExist as e:
            pass
    elif request.method == "PATCH":
        reqObj = json.loads(request.body.decode('utf-8'))
        # print(reqObj)
