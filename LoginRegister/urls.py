from django.urls import path
from LoginRegister import views
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve
urlpatterns = [
    path('login/',views.login),
    path('',views.index),
    path('register/',views.register),
    path('students/',views.userinfo),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),
	#url(r'^static/(?P<path>.*)$',  serve, {'document_root': settings.STATIC_ROOT })
    # url(r'^static/(?P<path>.*)$','django.views.static.server',{'document_root':settings.STATIC_URL})
]
