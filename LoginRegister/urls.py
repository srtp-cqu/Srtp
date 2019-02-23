from django.urls import path
from LoginRegister import views
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('students/',views.userinfo)
    #path('show/',views.show)
    # url(r'^static/(?P<path>.*)$','django.views.static.server',{'document_root':settings.STATIC_URL})
]