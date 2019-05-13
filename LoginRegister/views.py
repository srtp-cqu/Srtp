from django.shortcuts import render,HttpResponse,redirect,render_to_response
import os
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from LoginRegister import models
from django.http import Http404

# Create your views here.
def index(request):
    return render(request,'index.html')


def login(request):
    if request.method == 'GET':
        #return render(request,'login.html')
        raise Http404("你所访问的页面不存在")
        return render_to_response('404.html',status=404)
    if request.method == 'POST':
        username = request.POST['name']     #前端发送过来的学生学号/老师用户名
        type = request.POST['type']
        pwd = request.POST['pwd']
        print(username,type,pwd)
        if type == "students":
            obj = models.Students.objects.all().values('studentnum')
            stm = {'studentnum':username}
            if stm not in obj:
                print("not exist")
                return HttpResponse("not exist")
            else:
                obj1 = models.Students.objects.get(studentnum=username)
                if check_password(pwd,obj1.password):
                    stu = HttpResponse("/students/")
                    stu.set_cookie('studentnum',username,httponly=False)
                    stu.set_cookie('type',type,httponly=False)
                    return stu
                else:
                    return HttpResponse("password error")
        elif type == "drivers" :
            obj = models.Drivers.objects.all().values('name')
            name = {'name':username}
            print(type)
            if name not in obj:
                print("not exist")
                #context = {}
                #context['content'] = 'not exist'
                #return render(request, 'index.html', context)
                return HttpResponse("not exist")
            else:
                obj1 = models.Drivers.objects.get(name = username)
                if check_password(pwd,obj1.password):
                    fac = HttpResponse("/facerec/")
                    fac.set_cookie('username',username,httponly=False)
                    fac.set_cookie('type',type,httponly=False)
                    return fac
                else:
                    #context['content'] = ''
                    #context['status'] = 'password error'
                    #return render(request, 'index.html', context)
                    return HttpResponse("password error")
        else:
            obj = models.Teachers.objects.all().values('name')
            name = {'name':username}
            print(type)
            if name not in obj:
                print("not exist")
                #context = {}
                #context['content'] = 'not exist'
                #return render(request, 'index.html', context)
                return HttpResponse("not exist")
            else:
                obj1 = models.Teachers.objects.get(name = username)
                if check_password(pwd,obj1.password):
                    fac = HttpResponse("/facerec/")
                    fac.set_cookie('username',username,httponly=False)
                    fac.set_cookie('type',type,httponly=False)
                    return fac
                else:
                    #context['content'] = ''
                    #context['status'] = 'password error'
                    #return render(request, 'index.html', context)
                    return HttpResponse("password error")


def register(request):
    if request.method == 'GET':
    #    return render(request,'register.html')
        raise Http404("你所访问的页面不存在")
        return render_to_response('404.html',status=404)
    if request.method == 'POST':
        username = request.POST['name']
        type = request.POST['type']
        pwd = request.POST['pwd']
        dj_pwd = make_password(pwd)
        print(username,type,dj_pwd)
        if type == "students":
            stm = request.POST['studentnum']
            print(stm)
            obj = models.Students.objects.all().values('studentnum')
            stmobj = {'studentnum':stm}
            if stmobj in obj:
                print("already exist")
                #context = {}
                #context['content'] = 'not exist'
                #return render(request,'index.html',context)
                return HttpResponse("error")
            else:
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
                obj = models.Students(name=username,password=dj_pwd,studentnum = stm,imgpath=storePath)
                obj.save()
                return HttpResponse("success")
                #return redirect('/',302)
        elif type == "drivers" :
            obj = models.Drivers(name = username, password = dj_pwd)
            obj.save()
            return HttpResponse("success")
        else:
            obj = models.Teachers(name = username, password = dj_pwd)
            obj.save()
            return HttpResponse("success")
            #return redirect('/',302)


def userinfo(request):
    #c = request.COOKIES.get('username')
    t = request.COOKIES.get('type')
    if t != "students":
        return redirect('/',302)
    else:
        context = {}
        c = request.COOKIES.get('studentnum')
        obj = models.Students.objects.get(studentnum=c)
        imgPath = obj.imgpath
        username = obj.name
        money = obj.money
        print(imgPath)
        context['name'] = username
        context['studentnum'] = c
        context['img'] = imgPath
        context['money'] = money
    return render(request,'userinfo.html',context)