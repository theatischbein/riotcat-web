from django.db import models
from django.utils import timezone


class Types(models.TextChoices):
    WORK="Arbeit"
    ILL="Krank"
    FREE="Feiertag"
    HOLIDAY="Urlaub"
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategorie")

    def __str__(self):
        return self.name

class Work(models.Model):
    dateFrom = models.DateTimeField(default=timezone.now, verbose_name="Beginn")
    dateTo = models.DateTimeField(null=True, blank=True, verbose_name="Ende")
    category = models.ForeignKey("Category", verbose_name="Kategorie", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=[(tag, tag.value) for tag in Types], verbose_name="Typ")
    duration = models.IntegerField(null=True, blank=True, verbose_name="Dauer", default=0)

    def __str__(self):
        return "%s (%s, Dauer: %s)" %(self.dateFrom.strftime("%d.%m.%y"), self.type, self.duration)

    def calculateDuration(self):
        if self.dateTo:
            if self.type != Types.WORK:
                print((self.dateTo - self.dateFrom).days)
                return int(((self.dateTo - self.dateFrom).days + 1)* (40/30.5)) *24 * 60 * 60
            else:
                return int((self.dateTo - self.dateFrom).total_seconds())
        return 0

    class Meta:
        ordering = ['-dateFrom']
