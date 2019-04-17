### 说明
- autodeploy是用django开发的管理ansible任务的。
- 采用django开发的web后端，用vue开发的web前端。
- dist文件夹是编译后的前端资源文件，直接用django自带的python manage.py runserver运行就能访问
- 访问地址为http://127.0.0.1:8000/，用户名密码为: admin/admin
- 前端的项目为autodeploy-front,改动前端后需要重新编译生成dist文件夹替换本项目中的dist文件夹
- 需要将dist目录下的favicon.ico移动到dist/static下面。