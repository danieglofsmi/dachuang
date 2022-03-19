from django.urls import path
from django.urls import re_path
from . import views 
from django.conf.urls import include

urlpatterns = [
path("",views.index_in,name="index"),
#文件上传路由配置
path("upload",views.upload,name="upload"),#加载文件上传表单页
path("doupload",views.doupload,name="doupload"),#执行文件上传表单
]