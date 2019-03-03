import face_recognition
from math import sqrt
from os import listdir
from os.path import isdir, join, isfile, splitext
import pickle
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn import neighbors
from django.shortcuts import render
import os,base64
import requests as req
from django.conf import settings
from django.shortcuts import HttpResponse,redirect
from urllib import parse,request
import urllib
from io import BytesIO
# Create your views here.
ALLOWED_EXTENSTIONS = {'png','jpg','jpeg'}
LIST = []

def upload(request):
    return render(request,'upload.html')

	
def show():                               #获取所有的学生信息
    from LoginRegister import models
    user_list = models.Students.objects.all().values('name')
    us_list=list(user_list)
    user = []
    for us in user_list:
        user.append(us['name'])
    # print(type(user))
    # print(user)
    return user
	
	
def facerecpage(request):
    #c = request.COOKIES.get('username')
    t = request.COOKIES.get('type')
    if t != "teachers":
        return redirect('/', 302)
    if request.method == "GET":
        return render(request,'images.html')
    elif request.method == "POST":
        print("post")
        url = 'http://120.79.240.163:8000/takepic/'
        data_con = {'action':'takepic'}
        data = urllib.parse.urlencode(data_con).encode('utf-8')
        r = urllib.request.Request(url=url,data=data,headers={'content-Type':'application/x-www-form-rulencoded'})
        ans = urllib.request.urlopen(r).read().decode('utf-8')
        print(ans)
        # img_url = "http://holder.org:65530/static/img/image.jpg"
        # file_path = settings.MEDIA_ROOT+'/pic'
        # ext = os.path.splitext(img_url)[1]
        # file_name = "temp"
        # response = req.get(img_url)
        # image = Image.open(BytesIO(response.content))
        # ls_f = base64.b64encode(BytesIO(response.content).read())
        # print (type(ls_f))
        # imgdata = base64.b64decode(ls_f)
        # filepath = os.path.join(settings.MEDIA_ROOT+'/pic/',file_name+ext)
        # with open(filepath,'wb') as fp:
        #     fp.write(imgdata)
        # fp.close()
        return HttpResponse("success")

def uploadimg(request):
    all_user = show()
    lack = []
    LIST = []
    pic_user = []
    #f = request.FILES['image']
    img_url = request.POST.get('url')
    #filepath = os.path.join(settings.MEDIA_ROOT + '/pic/', f.name)
    file_path = settings.MEDIA_ROOT + '/pic'
    ext = os.path.splitext(img_url)[1]
    file_name = "temp"
    response = req.get(img_url)
    image = Image.open(BytesIO(response.content))
    ls_f = base64.b64encode(BytesIO(response.content).read())
    print(type(ls_f))
    imgdata = base64.b64decode(ls_f)
    filepath = os.path.join(settings.MEDIA_ROOT + '/pic/', file_name + ext)
    with open(filepath, 'wb') as fp:
        # for info in f.chunks():
        #     fp.write(info)
        #     knn_clf = train(settings.MEDIA_ROOT+'/train/')
        #     for img_path in listdir(settings.MEDIA_ROOT+'/pic/'):
        #         preds = predict(join(settings.MEDIA_ROOT+'/pic/', img_path), knn_clf=knn_clf)
        #         print(preds)
        #         LIST.append(preds)
        #     os.unlink(filepath)
        #     return HttpResponse(LIST)
        fp.write(imgdata)
    fp.close()
    knn_clf = train(settings.MEDIA_ROOT + '/train/')
    for img_path in listdir(settings.MEDIA_ROOT + '/pic/'):
        preds = predict(join(settings.MEDIA_ROOT + '/pic/', img_path), knn_clf=knn_clf)
        print(preds)
        LIST.append(preds)
    for person in preds:
        pic_user.append(person[0])
    print(pic_user)
    for user in all_user:
        if user not in pic_user:
            lack.append(user)
            lack.append(' ')
    print(lack)
    os.unlink(filepath)
    #return HttpResponse(LIST)
    return HttpResponse(lack)
	#return HttpResponse("failed")


def train(train_dir,model_save_path = "",n_neighbors = None,knn_algo = "ball_tree",verbose = False):
    X = []
    Y = []
    for class_dir in listdir(train_dir):
        if not isdir(join(train_dir,class_dir)):
            continue
        for img_path in image_files_in_folder(join(train_dir,class_dir)):
            image = face_recognition.load_image_file(img_path)
            faces_bboxes = face_locations(image)
            if len(faces_bboxes) != 1:
                if verbose:
                    print("image {} not fit for training: {}".format(img_path,"didn't find a face" if len(faces_bboxes) < 1 else "found more than one face"))
                continue
            X.append(face_recognition.face_encodings(image,known_face_locations=faces_bboxes)[0])
            Y.append(class_dir)

    if n_neighbors is None:
        n_neighbors = int(round(sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically as:",n_neighbors)

    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors,algorithm=knn_algo,weights='distance')
    knn_clf.fit(X,Y)

    if model_save_path != "":
        with open(model_save_path,'wb') as f:
            pickle.dump(knn_clf,f)
    return knn_clf


def predict(X_img_path,knn_clf = None,model_save_path = "",DIST_THRESH = .5):
    if not isfile(X_img_path) or splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSTIONS:
        raise Exception("invalid image path: {}".format(X_img_path))
    if knn_clf is None and model_save_path == "":
        raise Exception("must dupply knn classifier either thourgh knn_clf or model_save_path")
    if knn_clf is None:
        with open(model_save_path,'rb') as f:
            knn_clf = pickle.load(f)

    X_img = face_recognition.load_image_file(X_img_path)
    X_faces_loc = face_locations(X_img)
    if len(X_faces_loc) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_faces_loc)

    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

    is_recognized = [closest_distances[0][i][0] <= DIST_THRESH for i in range(len(X_faces_loc))]
    #return [(pred) if rec else ("N/A") for pred, rec in zip(knn_clf.predict(face_encodings),is_recognized)]
    return [(pred,loc) if rec else ("N/A",loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings),X_faces_loc,is_recognized)]
