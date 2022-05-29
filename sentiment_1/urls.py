"""sentiment_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from index import views
from visitors_book import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("index.urls")),
    path("visitors_book/", include("visitors_book.urls")),# path('visitors_book/', views.visitors_book, name='visitors_book'),
    path('visitors_book/today_emotion/', views.today_emotion, name='today_emotion'),
    path("music_choice/",include('music_choice.urls')),
]
