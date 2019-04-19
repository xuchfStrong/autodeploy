#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime
from django.shortcuts import render,redirect,HttpResponse,render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from webadmin.models import *
import webadmin.genrate_var_file
import webadmin.runner
# import webadmin.ansibleAPI
import sys
import os
import shutil
import json
import random

reload(sys)
sys.setdefaultencoding('utf-8')

PATH_CURRENT = os.path.abspath(__file__)
PATH_PARENT = os.path.dirname(PATH_CURRENT)
WORKHOME = os.path.dirname(PATH_PARENT)
HOSTSINVENTORY = WORKHOME+'/ansible/jieyun.hosts'
HOSTSINVENTORY_ALLSERVER = WORKHOME+'/ansible/init_server.hosts'
GROUPVAR = WORKHOME+'/ansible/group_vars/all.yml'
GROUPVAR_ALLSERVER = WORKHOME+'/ansible/group_vars/allserver.yml'
PLAYBOOK = WORKHOME+'/ansible/jieyun.yml'
PLAYBOOK_ALLSERVER = WORKHOME+'/ansible/init_server.yml'
TASK_LOGPATH = WORKHOME + '/tasklog/'
ANSIBLE_LOGPATH = '/var/log/ansible.log'


# Create your views here.

# 重写json的JSONEncoder，用来解决datetime格式的问题
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 分页
def page_info(list, page_size, page):
    # info格式 为 数据序列化后的json格式
    paginator = Paginator(list, page_size)
    try:
        page_data = paginator.page(page).object_list
    except PageNotAnInteger:
        page_data = paginator.page(1).object_list
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages).object_list

    return page_data


# dashboard页面
def dashboard(request):
    servercnt = Servers.objects.count()
    taskcnt = Tasks.objects.count()
    repocnt = Repository.objects.count()
    dbcnt = Databases.objects.count()
    task_list = Tasks.objects.all()
    data = {
        'servercnt': servercnt,
        'taskcnt': taskcnt,
        'repocnt': repocnt,
        'dbcnt': dbcnt
    }
    res = {'code': 20000, 'data': data}
    return JsonResponse(res, safe=True)


# 登录
def login(request):
    '''
    POST提交数据为json格式的时候，无法通过request.POST.get('username')获取到，
    需要先将request.body通过json.loads转为dict
    json.load 和 json.loads是有区别的
    :param request:
    :return:
    '''
    # csrftoken = request.COOKIES["csrftoken"]
    # print(csrftoken)
    json_data = json.loads(request.body)
    username = json_data['username']
    password = json_data['password']
    check_user = Users.objects.filter(username__exact=username, password__exact=password)
    if check_user:
        res = {'code': 20000, 'data':{'token': username}}
        return JsonResponse(res, safe=True)
    else:
        res = {'code': 20001, 'msg': '登陆失败'}
        return JsonResponse(res, safe=True)


# 查询用户信息
def userinfo(request):
    token = request.GET.get('token')
    data = {
        'roles': [token],
        'name' : token,
        'avatar': ''
    }
    res = {'code': 20000, 'data': data}
    return JsonResponse(res, safe=True)


# 退出
def logout(request):
    res = {'code': 20000, 'data': 'success'}
    return JsonResponse(res, safe=True)


# 获取服务器
def getserver(request):
    # server_set = Servers.objects.values()
    # res=list(server_set)
    total = Servers.objects.all().count()
    page = request.GET.get('page', 1)
    ip = request.GET.get('ip')
    page_size = request.GET.get('pagesize', '1')
    if ip:
        total = Servers.objects.filter(ip__exact=ip).count()
        server_set = Servers.objects.filter(ip__exact=ip).values()
    else:
        total = Servers.objects.all().count()
        server_set = Servers.objects.order_by('host_id').values()
    server_list = list(server_set)
    servers = page_info(server_list, page_size, page)
    data = { 'servers': servers, 'total': total}
    res = {'code': 20000, 'data': data }
    return JsonResponse(res, safe=True)  # 如果不设置safe=False，data必须为dict类型


# 添加服务器
def addserver(request):
    res = {}
    # get_token(request)  # 或request.META["CSRF_COOKIE_USED"] = True   新加产生token
    ip = request.GET['ip']
    hostname = request.GET['hostname']
    root_password = request.GET['root_password']

    if not all([ip, hostname, root_password]): # 判断字段是否为空
        res["code"] = 20001
        res["msg"] = "添加失败，字段不能为空"
        return JsonResponse(res, safe=True)
    elif Servers.objects.filter(ip__exact = ip): # 判断IP是否重复
        res["code"] = 20001
        res["msg"] = "添加失败，IP重复"
        return JsonResponse(res, safe=True)
    elif Servers.objects.filter(hostname__exact = hostname): # 判断主机名是否重复
        res["code"] = 20001
        res["msg"] = "添加失败，主机名重复"
        return JsonResponse(res, safe=True)
    else:
        try:
            Servers.objects.get_or_create(ip=ip, hostname=hostname, root_password=root_password)
            res["code"] = 20000
            res["msg"] = "添加成功"
        except Exception as e:
            res["code"] = 20001
            res["msg"] = e
        return JsonResponse(res, safe=True)


# 修改服务器
def editserver(request):
    res = {}
    host_id = request.GET['host_id']
    ip = request.GET['ip']
    hostname = request.GET['hostname']
    root_password = request.GET['root_password']

    if not all([ip, hostname, root_password]):
        res["code"] = 20001
        res["msg"] = "修改失败，字段不能为空"
        return JsonResponse(res, safe=True)
    elif Servers.objects.filter(Q(ip__exact = ip), ~Q(host_id__exact = host_id)):
        res["code"] = 20001
        res["msg"] = "修改失败，IP重复"
        return JsonResponse(res, safe=True)
    elif Servers.objects.filter(Q(hostname__exact = hostname), ~Q(host_id__exact = host_id)):
        res["code"] = 20001
        res["msg"] = "修改失败，主机名重复"
        return JsonResponse(res, safe=True)
    else:
        try:
            Servers.objects.filter(host_id=host_id).update(ip=ip, hostname=hostname, root_password=root_password)
            res["code"] = 20000
            res["msg"] = "修改成功"
        except Exception as e:
            res["code"] = 20001
            res["msg"] = e
        return JsonResponse(res, safe=True)


# 删除需要初始化的服务器
def delserver(request):
    host_id = request.GET['host_id']
    host_id_list = host_id.strip().split(',')
    for i in host_id_list:
        Servers.objects.filter(host_id=i).delete()
    res = {
        'code': 20000,
        'msg': '删除成功',
    }
    return JsonResponse(res, safe=True)


# 获取所有server
def getallserver(request):
    host_set = Servers.objects.values('ip', 'host_id')
    data = list(host_set)
    res = {'code': 20000, 'data':data}
    return JsonResponse(res, safe=True)


# 获取所有需要初始化的主机IP
def queryservers():
    result_list = [ ]
    host_set = Servers.objects.values_list('ip')
    for i in host_set:
        result_list.append(i[0].encode('utf-8'))
    result_str = ", ".join([str(x) for x in result_list])
    return result_str


# 初始化服务器
def initserver(request):
    data = {}
    server_list = queryservers()
    insertServer = InitServer.objects.create(server_list=server_list, status="Processing")
    gen_var_file = webadmin.genrate_var_file.genfile_all_server()
    init_result = webadmin.runner.run("initTest") # 测试
    # runtask = webadmin.ansibleAPI.PlayBook(None, None, HOSTSINVENTORY_ALLSERVER, PLAYBOOK_ALLSERVER)  # 调用API
    # init_result = runtask.playbookrun()  # 调用API
    InitServer.objects.filter(id=insertServer.id).update(status=init_result)
    if init_result == "Success":
        res = {'code': 20000, 'msg': '初始化成功'}
    else:
        res = {'code': 20001, 'msg': '初始化失败'}
    return JsonResponse(res, safe=True)


# 查看初始化状态
def initstatus(request):
    last = InitServer.objects.order_by('-id')[:1].values()
    # data = json.dumps(list(last), default=str)  # default=str的作用是让时间字段也能转为list
    data_json = json.dumps(list(last), cls=ComplexEncoder)
    data = json.loads(data_json)
    # return HttpResponse(data, content_type="application/json")
    res = {'code': 20000, 'data': data}
    return JsonResponse(res, safe=True)


# 获取服务列表
def getservice(request):
    service = request.GET.get('service')
    all = request.GET.get('all')
    if service:
        db_set = Services.objects.filter(service__exact=service).values('db_type').distinct()
        data = list(db_set)
        res = {'code': 20000, 'data':data}
        return JsonResponse(res, safe=True)
    elif all:
        srv_set = Services.objects.values('service').distinct()
        data = list(srv_set)
        res = {'code': 20000, 'data': data}
        return JsonResponse(res, safe=True)
    else:
        srv_set = Services.objects.filter(is_db__exact=True).values('service').distinct()
        data = list(srv_set)
        res = {'code': 20000, 'data': data}
        return JsonResponse(res, safe=True)


# 添加yum源信息
def addrepo(request):
    res = {}
    ip = request.GET.get('ip')
    port = request.GET.get('port')
    if not all([ip, port]): # 判断字段是否为空
        res["code"] = 20001
        res["msg"] = "添加失败，字段不能为空"
        return JsonResponse(res, safe=True)
    elif Repository.objects.all(): # 判断IP是否重复
        res["code"] = 20001
        res["msg"] = "添加失败，只能添加一条repo数据"
        return JsonResponse(res, safe=True)
    else:
        Repository.objects.get_or_create(ip=ip, port=port)
        res["code"] = 20000
        res["msg"] = "添加成功"
        return JsonResponse(res, safe=True)


# 删除yum源信息
def delrepo(request):
    repo_id = request.GET.get('repo_id')
    Repository.objects.filter(repo_id=repo_id).delete()
    res = {
        'code': 20000,
        'msg': '删除成功'
    }
    return JsonResponse(res, safe=False)


# 获取repo信息
def getrepo(request):
    repo_set = Repository.objects.values()
    data = list(repo_set)
    res = {'code': 20000, 'data':data}
    return JsonResponse(res, safe=True)


# 添加数据库信息
def adddb(request):
    res = {}
    srv_type = request.GET.get('srv_type')
    db_type = request.GET.get('db_type')
    root_password = request.GET.get('root_password')
    srv_password = request.GET.get('srv_password')

    if not all([srv_type, db_type, root_password, srv_password]): # 判断字段是否为空
        res["code"] = 20001
        res["msg"] = "添加失败，字段不能为空"
        return JsonResponse(res, safe=True)
    elif Databases.objects.filter(srv_type__exact = srv_type): # 判断IP是否重复
        res["code"] = 20001
        res["msg"] = "添加失败，一个业务只能添加一条数据库信息"
        return JsonResponse(res, safe=True)
    else:
        Databases.objects.get_or_create(srv_type=srv_type, db_type=db_type, root_password=root_password,
                                        srv_password=srv_password)
        res["code"] = 20000
        res["msg"] = "添加成功"
        return JsonResponse(res, safe=True)


# 删除数据库信息
def deldb(request):
    # Databases.objects.filter(db_id=db_id).delete()
    # return HttpResponseRedirect("/adddb/")
    db_id = request.GET.get('db_id')
    Databases.objects.filter(db_id=db_id).delete()
    res = {
        'code': 20000,
        'msg': '删除成功'
    }
    return JsonResponse(res, safe=False)


# 获取数据库信息
def getdb(request):
    db_set = Databases.objects.values()
    data = list(db_set)
    res = {'code': 20000, 'data':data}
    return JsonResponse(res, safe=True)


# 通过host_id查询主机列表
def queryhosts(list):
    result_list = [ ]
    host_set = Servers.objects.filter(host_id__in=list).values_list('ip')
    for i in host_set:
        result_list.append(i[0].encode('utf-8'))
    result_str = " ".join([str(x) for x in result_list])
    return result_str


# 创建任务
def createtask(request):
    srv_type = request.GET.get('service')
    host_id = request.GET['serverList']
    host_id_list = host_id.strip().split(',')
    if srv_type in ['ambari_server', 'zabbix_server'] and len(host_id_list) > 1:
        res = {
            'code': 20001,
            'msg': '该服务只能有一个主机',
        }
    else:
        host_list = queryhosts(host_id_list)
        Tasks.objects.get_or_create(srv_type=srv_type, host_id=host_id, host_list=host_list, task_status='NewTask')
        res = {
            'code': 20000,
            'msg': '创建成功',
        }
    return JsonResponse(res, safe=True)


def gettask(request):
    page = request.GET.get('page', 1)
    page_size = request.GET.get('pagesize', 10)
    total = Tasks.objects.all().count()
    task_set = Tasks.objects.order_by('-task_id').values()
    list_data = list(task_set)
    page_task = page_info(list_data, page_size, page)
    json_task = json.dumps(page_task, cls=ComplexEncoder)
    tasks = json.loads(json_task)
    data = {'tasks': tasks, 'total': total}
    res = {'code': 20000, 'data': data}
    return JsonResponse(res, safe=True)


# 删除任务
def deltask(request):
    task_id = request.GET['task_id']
    task_id_list = task_id.strip().split(',')
    for i in task_id_list:
        Tasks.objects.filter(task_id=i).delete()
    res = {
        'code': 20000,
        'msg': '删除成功',
    }
    return JsonResponse(res, safe=True)


# 执行任务
def runtask(request):
    task_id = request.GET.get('task_id')
    is_task_running = Tasks.objects.filter(task_status='Running').count()
    if not is_task_running:
        srv_type = Tasks.objects.values_list('srv_type', flat=True).get(task_id=task_id).encode("utf-8")
        task_status = Tasks.objects.values_list('task_status', flat=True).get(task_id=task_id)
        gen_var_file = webadmin.genrate_var_file.genfile(task_id.encode('utf-8'))

        if srv_type and gen_var_file and task_status == 'NewTask':
            Tasks.objects.filter(task_id=task_id).update(task_status='Running')
            result = webadmin.runner.run(srv_type) # 测试
            # runtask = webadmin.ansibleAPI.PlayBook(srv_type, None, HOSTSINVENTORY, PLAYBOOK) # 调用API
            # result = runtask.playbookrun()  # 调用API
            Tasks.objects.filter(task_id=task_id).update(task_status=result)
            if result == 'Success':
                res = {'code': 20000, 'msg': '执行成功'}
            else:
                res = {'code': 20001, 'msg': '执行失败'}

        # 将ansible.log拷贝到项目的目录，用于页面展示，并且在文件前后加入<pre>标签
        # shutil.copy(ANSIBLE_LOGPATH, os.path.join(TASK_LOGPATH, 'ansible%s.log' % task_id))
        # with open(os.path.join(TASK_LOGPATH, 'ansible%s.log' % task_id), "r+") as f:
        #     old = f.read()
        #     f.seek(0)
        #     f.write('<pre>' + '\n')
        #     f.write(old)
        #     f.seek(0, 2)
        #     f.write('</pre>' + '\n')
        # with open(ANSIBLE_LOGPATH, 'w+') as f:  # 清空ansible.log，以便记录下次任务日志
        #     f.close()
    else:
        res = {'code': 20001, 'msg': '有任务正在执行，请稍候'}

    return JsonResponse(res, safe=True)


# 查看日志
def viewlog(request):
    task_id = request.GET.get('task_id')
    task_status = Tasks.objects.values_list('task_status', flat=True).get(task_id__exact=task_id)
    if task_status == 'Running':
        with open(ANSIBLE_LOGPATH, "r+") as f:
            log_content = f.read()
        res = {
            'code': 20000,
            'data': log_content
        }
    else:
        with open(os.path.join(TASK_LOGPATH, 'ansible%s.log' % task_id), "r+") as f:
            log_content = f.read()
        res = {
            'code': 20000,
            'data': log_content
        }
    return JsonResponse(res, safe=True)


# 预处理日志,作废
def pre_log(file_path):
    shutil.copy(file_path, os.path.join(TASK_LOGPATH, 'ansible_tmp.log'))
    with open(os.path.join(TASK_LOGPATH, 'ansible_tmp.log'), "r+") as f:
        old = f.read()
        f.seek(0)
        f.write('<pre>' + '\n')
        f.seek(0, 2)
        f.write('</pre>' + '\n')
    with open(os.path.join(TASK_LOGPATH, 'ansible_tmp.log'), "r") as f2:
        content = f2.read()
    os.remove(os.path.join(TASK_LOGPATH, 'ansible_tmp.log'))
    return content

# 文件上传
def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("file", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            res = {
                'code': 20001,
                'msg': '上传失败',
                'success': False
            }
        else:
            destination = open(os.path.join(TASK_LOGPATH,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():      # 分块写入文件
                destination.write(chunk)
            destination.close()
            res = {
                'code': 20000,
                'msg': '上传成功',
                'success': random.choice([True, False])
            }
        return JsonResponse(res, safe=True)

# 文件下载
def download_file(request):
    id = request.GET.get('id')
    if id == '1':
        filename = 'favicon.ico'
    else:
        filename = 'ansible128.log'
    file = open(os.path.join(TASK_LOGPATH, filename), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' %(filename)
    return response