from django.shortcuts import render,HttpResponse
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from LoginRegister import models
# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        username = request.POST['name']
        type = request.POST['type']
        pwd = request.POST['pwd']
        print(username,type,pwd)
        return HttpResponse("ok")


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    if request.method == 'POST':
        username = request.POST['name']
        type = request.POST['type']
        pwd = request.POST['pwd']
        dj_pwd = make_password(pwd)
        print(username,type,dj_pwd)
        if type == "students":
            f = request.FILES['img']
            ext = os.path.splitext(f.name)[1]
            startPath = settings.MEDIA_ROOT+'/train'
            targetPath = startPath+os.path.sep+username
            print(targetPath)
            if not os.path.exists(targetPath):
                os.makedirs(targetPath)
            filePath = os.path.join(targetPath+os.path.sep,username+ext)
            storePath = 'media/train/'+username+os.path.sep+username+ext
            with open(filePath,'wb') as fp:
                for info in f.chunks():
                    fp.write(info)
            obj = models.Students(name=username,password=dj_pwd,imgpath=storePath)
            obj.save()
            return render(request,'login.html')
        else:
            obj = models.Teachers(name=username,password=dj_pwd)
            obj.save()
            return render(request,'login.html')