import datetime
from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=200)
    login = models.CharField(max_length=100)
    status = models.BooleanField()
    registration = models.BooleanField()

    def __str__(self):
        return self.title

class ServicePort(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    number = models.IntegerField()
    protocol = models.CharField(max_length=50)

    def __str__(self):
        return "%s %s" %(self.number, self.protocol)

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    xmpp = models.CharField(max_length=100)
    matrix = models.CharField(max_length=100)
    pgp = models.TextField()

    def __str__(self):
        return self.name

class Blogentry(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return "%s - %s (%s)" %(self.title, self.author, self.pub_date.strftime("%d.%m.%Y"))
