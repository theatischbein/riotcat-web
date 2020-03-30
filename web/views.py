from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Service, ServicePort, Blogentry, Author

# Create your views here.
def index(request):
    service_list = Service.objects.all()
    blog_list = Blogentry.objects.order_by("-pub_date")
    contact = Author.objects.get(name="Jonny")
    template = loader.get_template('web/index.html')
    context = {
        'service_list': service_list,
        'blog_list': blog_list,
        'contact': contact,
    }
    return HttpResponse(template.render(context, request))