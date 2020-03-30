from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
from .models import Service, ServicePort, Author, Blogentry

class ServicePortInline(admin.TabularInline):
    model = ServicePort

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    inlines = [ServicePortInline,]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Blogentry)
admin.site.register(Author)