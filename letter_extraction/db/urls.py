from django.urls import path
from . import views

app_name = 'db'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),
    path('result/', views.search_result, name='result'),
    path('login/', views.login, name='login'),
    path('upload/scanfile/', views.upload, name='scanfile'),
]

