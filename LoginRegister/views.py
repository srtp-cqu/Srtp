from django.shortcuts import render,HttpResponse,redirect
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from LoginRegister import models
# Create your views here.
def index(request):
    return render(request,'index.html')

	
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        username = request.POST['name']
        type = request.POST['type']
        pwd = request.POST['pwd']
        print(username,type,pwd)
        context = {}
        context['content'] = ''
        context['status'] = ''
        if type == "students":
            obj = models.Students.objects.all().values('name')
            print(obj)
            name = {'name':username}
            if name not in obj:
                print("not exist")
                context = {}
                context['content'] = 'not exist'
                return render(request,'login.html',context)
            else:
                obj1 = models.Students.objects.get(name=username)
                print(obj1.password)
                print(check_password('987698',obj1.password))
                if check_password(pwd,obj1.password):
                    stu = redirect('/students/',302)
                    stu.set_cookie('username',username,httponly=False)
                    stu.set_cookie('type',type,httponly=False)
                    return stu
                else:
                    context['content'] = ''
                    context['status'] = 'password error'
                    return render(request,'login.html',context)
        else:
            obj = models.Teachers.objects.all().values('name')
            name = {'name':username}
            print(type)
            if name not in obj:
                print("not exist")
                context = {}
                context['content'] = 'not exist'
                return render(request, 'login.html', context)
            else:
                obj1 = models.Teachers.objects.get(name = username)
                if check_password(pwd,obj1.password):
                    fac = redirect('/facerec/',302)
                    fac.set_cookie('username',username,httponly=False)
                    fac.set_cookie('type',type,httponly=False)
                    return fac
                else:
                    context['content'] = ''
                    context['status'] = 'password error'
                    return render(request, 'login.html', context)


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
            return redirect('/',302)
        else:
            obj = models.Teachers(name=username,password=dj_pwd)
            obj.save()
            return redirect('/',302)


def userinfo(request):
    #c = request.COOKIES.get('username')
    t = request.COOKIES.get('type')
    if t != "students":
        return redirect('/',302)
    return render(request,'userinfo.html')