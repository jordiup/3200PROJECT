from django.urls import path
from . import views

app_name = 'db'
urlpatterns = [
    #path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),
    path('result/', views.search_result, name='result'),
    path('login/', views.login_user, name='login'),
    path('upload/scanfile/', views.upload, name='scanfile'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name = 'test')
]
