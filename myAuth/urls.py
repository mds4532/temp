from django.urls import path, re_path
from . import views
from .models import Texts
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'^auth', views.auth, name='auth'),
    re_path(r'^registration', views.registration, name='reg'),
    path('account/', views.account, name="account"),
    path('editable/<int:pk>', views.editText, name='edit'),
    path('editable/', views.createText, name='create')
]