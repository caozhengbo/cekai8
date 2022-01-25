# AutoTest_Web


> AutoTest_Web that depends AutoTest_Server

## 本地开发环境部署

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

```

测试
-----------

1. open url(recommend chrome): http://localhost:8080/testrunner/register

## 部署 nginx模式
--------------
1. 修改default.conf配置文件 server_name的ip(宿主机IP), 端口默认8080
2. 修改/src/restful/api.js baseUrl地址, 即为AutoTest_Web运行的宿主机地址
3. 执行npm install, npm run build # 生成生产环境包
4. 把default.conf配置文件放到nginx的conf.d目录下 mv default.conf /etc/nginx/conf.d/autotest.conf
5. 把构建的dist文件放到 default.conf配置的文件路径下，cp -r dist/*  /usr/share/nginx/html/
6. 运行nginx 
5. open url: http://宿主机ip:8080/testrunner/register
