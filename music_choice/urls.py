from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'music_choice'

urlpatterns = [
    path('', views.music_choice, name='music_choice'),
    path('recommendation/', views.recommendation, name='recommendation'),
]
