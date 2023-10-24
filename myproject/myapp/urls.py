from django.urls import path   
from . import views

urlpatterns = [
    path('', views.index, name='index'), #root url
    path('upload', views.upload_image, name='upload'),
    path('confirm_delete/<int:pk>', views.confirm_delete, name='confirm_delete'),
    path('view_image/<int:pk>', views.view_image, name='view_image'), 
    path('update_image/<int:pk>', views.update_image, name='update_image'), 

]