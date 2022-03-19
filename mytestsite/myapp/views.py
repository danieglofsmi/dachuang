import time
from django.shortcuts import render
from django.http import HttpResponse
#from django.http import JsonResponse
import requests
import json
#from requests.exceptions import HTTPError

# app主页
def index_in(request):
    return render(request, "myapp/index.html")

# 加载文件上传表单
def upload(request):
    return render(request, "myapp/upload.html")

# 执行文件上传处理
def doupload(request):
# 接收
    myfile = request.FILES.get("doc", None)
    if not myfile:
        return HttpResponse("file not find")
    print(myfile)
# 读入文件信息并写入,通过时间戳保留文件格式并生成文件名
    filename = str(time.time())+"."+myfile.name.split('.').pop()
    destination = open("./static/docs/"+filename, "wb+")
# 将文件流分块读取文件内容并写入目标文件
    for chunk in myfile.chunks():
        destination.write(chunk)
    destination.close

# 接收普通数据
#    print(request.POST.get("title"))
#   return HttpResponse("上传成功！"+filename) #页面信息

# 将地址转为json返回
    address = {"wave_file_path": "./static/docs/"+filename}

    host = "http://httpbin.org/"
    endpoint = "post"
    url = ''.join([host, endpoint])

    r = requests.post(url, json=json.dumps(address))
    # r = requests.post(url,data=json.dumps(address))  
    response = r.json()
    print(response)
#    return HttpResponse(json.dumps(address), content_type="application/json")
#    return HttpResponse(response)
#   return render(request,'myapp/upload.html',{"json_dict":response})
    return render(request,'output.html',{"json_out":response})
  
    