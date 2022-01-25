from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from test_user.models import UserModel


# Create your views here.


def login(request):
    if request.method == "POST":

        reqObj = json.loads(request.body.decode('utf-8'))
        # {'username': 'sgewg', 'password': 'sgwefe'}
        status, msg, user_obj = UserModel.objects.login(**reqObj)
        print(status, msg, user_obj)
        if not status:
            return JsonResponse({"success": status, "msg": msg})
        else:
            data = {
                "success": True,
                "token": user_obj.token_key,
                "user": user_obj.username,
                "name": user_obj.name,
            }
            return JsonResponse(data)
    """
    # 把代码实现封装起来了
    reqObj = json.loads(request.body.decode('utf-8'))
    username = reqObj.get('username')
    password = reqObj.get('password')

    try:

        # 判断username是否存在，
        user = UserModel.objects.get(username=username)
        # 如果username存在，则验证密码是否正确
        if user.password != password:
            data = {
                "success": False,
                "user": "",
                # "token": "sdfghjk",
                "msg": "密码错误"
            }
            return JsonResponse(data)
        else:
            data = {
                "success": True,
                "username": user.username,
                "user": user.name,
                "token": "sdfghjk",
                "msg": "登陆成功"
            }
            return JsonResponse(data)

    except UserModel.DoesNotExist as e:
        data = {
            "success": False,
            "user": "",
            "msg": "用户不存在",
            "Error": ""
        }
        return JsonResponse(data)
    """


def register(request):
    if request.method == "POST":
        reqObj = json.loads(request.body.decode("utf-8"))
        print("register_data:", reqObj)
        # b'{"username":"gewgwef","password":"123456","name":"wegweg","repwd":"123456","email":"sunck@qq.com"}'
        status, user_obj, msg = UserModel.objects.creat_user(**reqObj)
        return JsonResponse({"success": status, "msg": msg})
    """
    # 把实现内容进行封装
        if request.method == "POST":
        # print(request.POST)  # 传过来是空的
        print(request.body)  # 获取前端传过来的值  <class 'bytes'>  需要手动转一下到dict
        reqObj = json.loads(request.body.decode('utf-8'))
        # b'{"username":"admin","password":"123456","name":"123123","repwd":"123456","email":"2283841369@qq.com"}'  <class 'bytes'>

        # 查看用户账号是否可注册
        # select * from users where username=username
        response_username = reqObj.get("username")
        try:
            UserModel.objects.get(username=response_username)
            data = {
                "success": False,
                "msg": "该用户已经存在！！！"
            }
            return JsonResponse(data)
        except UserModel.DoesNotExist as e:
            # 可以注册，创建用户对象并保存到数据库
            print("可以进行注册")

            # del reqObj[]
            print(reqObj["repwd"])

            # 方法2
            # UserModel.objects.create(
            #     username=response_username,
            #     password=reqObj.get("password"),
            #     name=reqObj.get("name"),
            #     email=reqObj.get("email")
            # )
            # 最终方法  直接把response的数据用过create进行写入
            del reqObj["repwd"]  # 删掉字典中repwd字段
            UserModel.objects.create(**reqObj)
            data = {
                "success": True,
                "msg": "注册成功"
            }
            return JsonResponse(data)
    """
