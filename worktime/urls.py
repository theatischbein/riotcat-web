from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import models, views

urlpatterns = [
    path('', views.WorkView.as_view(), name="worktime_index"),
    path('new', views.WorkCreateView.as_view(), name="worktime_new"),
    path('end/<int:id>', views.WorkEnd, name="worktime_end"),
    path('edit/<int:pk>', views.WorkUpdateView.as_view(), name="worktime_edit"),
    path('delete/<int:id>', views.deleteWork, name="worktime_delete"),
    path('install', views.install),
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
