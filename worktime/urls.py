from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import models, views

urlpatterns = [
    path('', views.WorkView.as_view(), name="worktime_index"),
    path('worktime/change_category/<int:id>', views.change_category, name="worktime_index_category"),
    path('worktime/new', views.WorkCreateView.as_view(), name="worktime_new"),
    path('worktime/end/<int:id>', views.WorkEnd, name="worktime_end"),
    path('worktime/edit/<int:pk>', views.WorkUpdateView.as_view(), name="worktime_edit"),
    path('worktime/delete/<int:pk>', views.WorkDeleteView.as_view(), name="worktime_delete"),
    path('category', views.CategoryView.as_view(), name="category_index"),
    path('category/new', views.CategoryCreateView.as_view(), name="category_new"),
    path('category/edit/<int:pk>', views.CategoryUpdateView.as_view(), name="category_edit"),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name="category_delete"),
    #path('install', views.install),
]
#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
