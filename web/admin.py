from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from . import forms

# Register your models here.
from .models import Service, ServicePort, Author, Blogentry, FlatViewing

class ServicePortInline(admin.TabularInline):
    model = ServicePort

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    inlines = [ServicePortInline,]

class BlogentryAdmin(admin.ModelAdmin):
    form = forms.BlogentryForm

admin.site.register(Service, ServiceAdmin)
admin.site.register(Blogentry, BlogentryAdmin)
admin.site.register(Author)
admin.site.register(FlatViewing)