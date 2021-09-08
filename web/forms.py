from django import forms
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

from . import models

class BlogentryForm(forms.ModelForm):
    class Meta:
        model = models.Blogentry
        fields = '__all__'
        widgets = {'body': CKEditorWidget()}
