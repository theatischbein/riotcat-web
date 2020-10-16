from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime, timedelta


from .models import Service, ServicePort, Blogentry, Author

# Create your views here.
def index(request):
    service_list = Service.objects.all()
    blog_list = Blogentry.objects.order_by("-pub_date")
    contact = Author.objects.get(name="Jonny")
    template = loader.get_template('web/index.html')
    new_blogs = Blogentry.objects.filter(pub_date__gte=datetime.now()-timedelta(days=30)).count
    context = {
        'service_list': service_list,
        'blog_list': blog_list,
        'contact': contact,
        'count_new_blogs': new_blogs,
    }
    return HttpResponse(template.render(context, request))