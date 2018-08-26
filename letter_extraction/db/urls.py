from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

app_name = 'db'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('upload/', views.upload, name='upload'),
    path('result/', views.search_result, name='result'),
    path('login/', views.login, name='login'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

