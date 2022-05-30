from django.urls import path
from . import views # 같은 폴더 내의 views.py를 import

app_name = 'visitors_book'

urlpatterns = [
    path('', views.visitors_book, name='index'),
]
