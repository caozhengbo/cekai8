from django.db import models
from test_user.utils import secret  # 加密类

# Create your models here.

"""
python manage.py makemigrations
python manage.py migrate
"""


class BaseMode(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # 表示夫模型不在数据中生成表，而是将属性写入到子模型的表中


# 模型
class UserManager(models.Manager):

    # 给密码进行加密
    # _ 下划线的意思：  __私有属性 只能在当前类进行使用   _本质上是共有的，其实是可以在外面的类中使用，通俗会认为成私有的
    # 给密码加密
    def _encryption_passwd(self, passwd):
        return secret.encryption(passwd)

    # 验证密码的正确性 ：把获取到的密码加密后，在和数据库中加密的密码进行匹配
    def check_passwd(self, id, passwd):
        user = UserModel.objects.get(pk=id)
        return self._encryption_passwd(passwd) == user.password

    # 创建用户
    def creat_user(self, **kwargs):
        username = kwargs['username']
        try:
            UserModel.objects.get(username=username)
            status, user_obj, msg = False, None, "该用户已存在"
            return status, user_obj, msg
        except UserModel.DoesNotExist as e:
            email = kwargs['email']
            try:
                UserModel.objects.get(email=email)
                status, user_obj, msg = False, None, "该邮箱已存在"
                return status, user_obj, msg
            except UserModel.DoesNotExist as e:
                del kwargs['repwd']  # 删除重复验证密码的字段
                kwargs['password'] = self._encryption_passwd(kwargs['password'])  # 给密码进行加密
                user_obj = UserModel.objects.create(**kwargs)
                status, user_obj, msg = True, user_obj, "注册成功"
                return status, user_obj, msg

    # 修改token
    def _change_token(self, user_obj):
        user_obj.token_key = secret.random_key()  # 给token做一个加密,并写入到数据库
        user_obj.save()
        return user_obj

    # 登陆
    def login(self, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = UserModel.objects.get(username=username)
            # 如果用户存在，则进行密码验证
            if not self.check_passwd(user.id, password):
                return False, "密码错误", None
            else:
                # 密码相同 登陆成功
                self._change_token(user)  # token加密，并写入数据库
                return True, "登陆成功", user
        except UserModel.DoesNotExist as e:
            return False, "用户名不存在", None

    # 退出
    def quit(self):
        pass


class UserModel(BaseMode):
    # objects = UserManager  # 这里默认就会调用   # 如果没有显示定义模型管理对象的属性，会自动给模型添加一个名为objects的属性
    objects = UserManager()
    # 用户名(唯一的，不能为空)
    # 姓名（不能为空）
    # 密码（不存储明文，应存储密文）
    # 邮箱(唯一的，不能为空)
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=20, null=False, default="无")
    email = models.EmailField(unique=True, null=False)

    token_key = models.CharField(max_length=1000, null=True, default=None)  # 用于验证是否是登录状态

    class Meta:
        db_table = "user"
