from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bor76', views.flatviewing, name="flatviewing"),
]