from django.urls import path   
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('upload', views.upload_image, name='upload'),
    # path('details', views.details, name='details'),
]