"""autodeploy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webadmin import views as webadmin_views
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^dashboard/$', webadmin_views.dashboard, name='dashboard'),
    url(r'^user/login$', webadmin_views.login, name='login'),
    url(r'^user/info$', webadmin_views.userinfo, name='userinfo'),
    url(r'^user/logout$', webadmin_views.logout, name='logout'),
    url(r'^addserver/$', webadmin_views.addserver, name='addserver'),
    url(r'^delserver/$', webadmin_views.delserver, name='delserver'),
    url(r'^getserver/$', webadmin_views.getserver, name='getserver'),
    url(r'^editserver/$', webadmin_views.editserver, name='editserver'),
    url(r'^getallserver/$', webadmin_views.getallserver, name='getallserver'),
    url(r'^initserver/$', webadmin_views.initserver, name='initserver'),
    url(r'^initstatus/$', webadmin_views.initstatus, name='initstatus'),
    url(r'^getservice/$', webadmin_views.getservice, name='getservice'),
    url(r'^addrepo/$', webadmin_views.addrepo, name='addrepo'),
    url(r'^delrepo/$', webadmin_views.delrepo, name='delrepo'),
    url(r'^getrepo/$', webadmin_views.getrepo, name='getrepo'),
    url(r'^adddb/$', webadmin_views.adddb, name='adddb'),
    url(r'^deldb/$', webadmin_views.deldb, name='deldb'),
    url(r'^getdb/$', webadmin_views.getdb, name='getdb'),
    url(r'^createtask/$', webadmin_views.createtask, name='createtask'),
    url(r'^gettask/$', webadmin_views.gettask, name='gettask'),
    url(r'^deltask/$', webadmin_views.deltask, name='deltask'),
    url(r'^runtask/$', webadmin_views.runtask, name='runtask'),
    url(r'^viewlog/$', webadmin_views.viewlog, name='viewlog'),
    url(r'^favicon.ico', RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^upload/$', webadmin_views.upload_file, name='upload_file'),

]
