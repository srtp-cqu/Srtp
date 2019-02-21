import face_recognition
from math import sqrt
from os import listdir
from os.path import isdir, join, isfile, splitext
import pickle
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from face_recognition import face_locations
from face_recognition.cli import image_files_in_folder
from sklearn import neighbors
from django.shortcuts import render
import os
from django.conf import settings
from django.shortcuts import HttpResponse
# Create your views here.
ALLOWED_EXTENSTIONS = {'png','jpg','jepg'}
LIST = []

def upload(request):
    return render(request,'upload.html')


def uploadimg(request):
    LIST = []
    f = request.FILES['image']
    filepath = os.path.join(settings.MEDIA_ROOT + '/pic/', f.name)
    with open(filepath, 'wb') as fp:
        for info in f.chunks():
            fp.write(info)
            knn_clf = train(settings.MEDIA_ROOT+'/train/')
            for img_path in listdir(settings.MEDIA_ROOT+'/pic/'):
                preds = predict(join(settings.MEDIA_ROOT+'/pic/', img_path), knn_clf=knn_clf)
                print(preds)
                LIST.append(preds)
            return HttpResponse(LIST)
    return HttpResponse("failed")


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

    return [(pred,loc) if rec else ("N/A",loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings),X_faces_loc,is_recognized)]
