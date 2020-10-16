from django.core.exceptions import ValidationError
from django.db.models import Q
from django import forms
import datetime
from . import models

class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = models.Work
        fields = ['category', 'type', 'dateFrom', 'dateTo']

    def __init__(self, *args, **kwargs):
        super(WorkCreateForm, self).__init__(*args, **kwargs)
        self.initial['category'] = models.Category.objects.first()
        self.initial['type'] = models.Types.WORK

    def clean(self):
        cleaned_data = super(WorkCreateForm, self).clean()
        if models.Work.objects.filter(type=models.Types.WORK).filter(dateTo__isnull=True).all() and cleaned_data["type"] == models.Types.WORK:
            raise ValidationError("Es existiert noch ein nicht abgeschlossener Arbeitszeitraum!")


class WorkUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Work
        fields = ['dateFrom', 'dateTo', 'category', 'type', 'duration']

    def save(self, commit=True):
        work = super(WorkUpdateForm, self).save(commit=False)
        print(work.dateTo)
        work.duration = work.calculateDuration()

        if commit:
            work.save()
        return work

