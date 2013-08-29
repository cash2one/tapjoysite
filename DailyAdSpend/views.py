# Create your views here.
from django.shortcuts import render
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
import os, mimetypes


def partner_dir(partner_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report', partner_name)

def partnerindex(request):
    partner_links = filter( lambda f: not f.startswith('.'), os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')))
    return render(request, 'DailyAdSpend/partners.html', {'partners': partner_links})

def month(request, partner_name):
    month_links = filter( lambda f: not f.startswith('.'), os.listdir(partner_dir(partner_name)))
    return render(request, 'DailyAdSpend/month.html', {'months': month_links})

def day(request, partner_name, month):
    day_links = os.listdir(os.path.join(partner_dir(partner_name), month))
    return render(request, 'DailyAdSpend/day.html', {'days': day_links, 'month': month})


def download(request, partner_name, month, day):
    filename = os.path.join(partner_dir(partner_name), month, day)
    download_name = day
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)    
    response['Content-Disposition'] = "attachment; filename= {0}".format(download_name)
    return response
