from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_file, name='file_upload'),
    path('resize/<int:image_id>', views.resize_image, name='resize_image'),
    path('', views.mainpage, name='home')
]
