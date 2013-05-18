# Create your views here.
from django.shortcuts import render
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
import os, mimetypes

BASEDIR = 'ElexTech/report'
def month(request):
    month_links = filter( lambda f: not f.startswith('.'), os.listdir(BASEDIR))
    return render(request, 'month.html', {'months': month_links})

def day(request, month):
    day_links = os.listdir(os.path.join(BASEDIR, month))
    return render(request, 'day.html', {'days': day_links, 'month': month})


def download(request, month, day):
    filename = os.path.join(BASEDIR, month, day)
    download_name = day
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename= {0}".format(download_name)
    return response
