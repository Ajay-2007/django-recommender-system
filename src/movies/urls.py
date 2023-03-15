from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.movie_list_view),
    path('<int:pk>/', views.movie_detail_view),
]

