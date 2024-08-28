from django.core.exceptions import ValidationError
from django import forms

from . import models


class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = models.Work
        fields = ['category', 'type', 'dateFrom', 'dateTo']

    def __init__(self, *args, **kwargs):
        super(WorkCreateForm, self).__init__(*args, **kwargs)
        self.initial['category'] = kwargs["initial"]["current_category"]
        self.initial['type'] = models.Types.WORK

    def clean(self):
        cleaned_data = super(WorkCreateForm, self).clean()
        if models.Work.objects.filter(type=models.Types.WORK)\
                .filter(dateTo__isnull=True).all() \
                and cleaned_data["type"] == models.Types.WORK:
                    raise ValidationError(
                            "Es existiert noch ein nicht abgeschlossener Arbeitszeitraum!"
                            )

    def save(self, commit=True):
        work = super(WorkCreateForm, self).save(commit=False)
        work.duration = work.calculateDuration()

        if commit:
            work.save()
        return work


class WorkUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Work
        fields = ['dateFrom', 'dateTo', 'category', 'type', 'duration']

    def save(self, commit=True):
        work = super(WorkUpdateForm, self).save(commit=False)
        work.duration = work.calculateDuration()

        if commit:
            work.save()
        return work


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']
