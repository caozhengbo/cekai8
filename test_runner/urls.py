from django.urls import path, re_path
from test_runner.views import project, variable, hostip, config, tree, pycode, api, test

urlpatterns = [
    # 项目相关
    re_path(r'project/$', project.project1),  # get post delete patch
    re_path(r'project/(?P<pk>\d+)/$', project.project2),  # get

    re_path(r'gettagcount/$', project.gettagcount),
    re_path(r'getreporttail/$', project.getreporttail),

    re_path(r'variables/$', variable.variables),
    re_path(r'variables/(?P<pk>\d+)/$', variable.variables1),

    re_path(r'host_ip/$', hostip.host),
    re_path(r'host_ip/(?P<pk>\d+)/$', hostip.host1),

    re_path(r'config/$', config.config),
    re_path(r'config/(?P<pk>\d+)/$', config.config1),

    # re_path(r'tree//$', tree.tree),
    re_path(r'^tree/(?P<pk>\d+)/$', tree.tree1),

    re_path(r'api/$', api.api1),
    re_path(r'api/(?P<pk>\d+)/$', api.api2),
    re_path(r'run_api_pk/(?P<pk>\d+)/$', api.api3),

    re_path(r'^pycode/$', pycode.pycode1),
    re_path(r'^pycode/(?P<pk>\d+)/$', pycode.pycode2),
    re_path(r'^runpycode/(?P<pk>\d+)/$', pycode.runpycode),

    re_path(r'test/$', test.test1),
    re_path(r'test/(?P<pk>\d+)/$', test.test2),

    # re_path(r"^api_test/$", api.api4),

]
