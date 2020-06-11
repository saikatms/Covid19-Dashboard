from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('', views.index, name='home'),
]