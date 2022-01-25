# 中间件 验证是否登陆的

from django.utils.deprecation import MiddlewareMixin


class IsLoginMiddleware(MiddlewareMixin):# 需要在配置文件中注册
    def process_request(self, request):
        # 会在创建request对象之后，匹配路由之前被调用
        print("this is IsLoginMiddleware")
