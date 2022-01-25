import json

from test_runner import models
from django.http import JsonResponse
from test_runner.utils import parser, loader
from test_runner.utils.hostUtils import parse_host


def api1(request):
    if request.method == "GET":
        # <QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'node': [''], 'project': ['13'], 'search': ['']}>
        # print(request.GET)
        node = request.GET.get("node")
        project = request.GET.get("project")
        # project = models.ProjectMode.objects.get(pk=request.GET.get("project"))
        search = request.GET.get("search")

        apis = models.ApiModel.objects.filter(project_id=project).order_by("-update_time")
        if node:
            apis = apis.filter(relation=node)
        if search:
            apis = apis.filter(name__contains=search)
        apis = apis.values()

        data = {
            "count": len(apis),
            "results": list(apis)
        }
        return JsonResponse(data)
    elif request.method == "POST":
        reqObj = json.loads(request.body.decode('utf-8'))
        api = parser.Format(reqObj, level='test')
        api.parse()
        # print(api.testcase)
        # {'name': 'test', 'times': 1, 'request': {'url': '/api/test', 'method': 'POST', 'verify': False, 'json': {'name': 1}}, 'desc': {'header': {}, 'data': {}, 'files': {}, 'params': {}, 'variables': {}, 'extract': {}}}
        project = models.ProjectMode.objects.get(pk=api.project)
        models.ApiModel.objects.create(name=api.name,
                                       body=api.testcase,
                                       url=api.url,
                                       method=api.method,
                                       project=project,
                                       relation=api.relation)
        data = {
            "success": True
        }
        return JsonResponse(data)
    elif request.method == "DELETE":
        pass


def api2(request, pk):
    if request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass
    elif request.method == "GET":
        pass


def api3(request, pk):
    # if request.method == "GET":
    # <QueryDict: {'token': ['84bfacc1486cb1bf94d4e18be7478fea'], 'host': ['请选择'], 'config': ['请选择']}>
    # 2
    api = models.ApiModel.objects.get(pk=int(pk))
    host = request.GET.get("host")
    name = request.GET.get("config")
    if name == "请选择":
        config = None
    if host == "请选择":
        host = None

    testcase = eval(api.body)
    print(testcase)
    # 为了运行api的发起请求的，summary运行结果
    # def parse_tests(testcases, debugtalk, project, name=None, config=None):

    summary = loader.debug_api(testcase, api.project_id, config=parse_host(host, config))
    print("summary:", summary)  # SyntaxError: HttpRunner() takes no arguments
    return JsonResponse(summary)

# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# # @csrf_exempt
# # def api4(request):
# #     return HttpResponse({"data": 123})
# @csrf_exempt
# def api4(request):
#     dic = {}
#     if request.method == 'GET':
#         dic['message'] = 0
#         return HttpResponse(json.dumps(dic))
#     else:
#         dic['message'] = '方法错误'
#         return HttpResponse(json.dumps(dic, ensure_ascii=False))
