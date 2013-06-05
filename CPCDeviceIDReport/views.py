# Create your views here.

import uuid, time
import os, sys, mimetypes
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from CPCDeviceIDReport.forms import QueryForm
from CPCDeviceIDReport.report import generateReport

def query_form(request):
    if 'adID' in request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            #html = []
            #for k,v in cd.items():
            #    html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
            request.session['queryID'] = str(uuid.uuid1())
            request.session['adID'] = str(cd['adID'])
            request.session['startDate'] = str(cd['startDate'])
            request.session['endDate'] = str(cd['endDate'])
            request.session['macFormat'] = str(cd['macFormat'])
            return render_to_response('query_in_progress.html', 
                                      {'queryID':request.session['queryID'], 
                                       'adID': cd['adID'], 
                                       'startDate':cd['startDate'], 
                                       'endDate': cd['endDate'],
                                       'macFormat': cd['macFormat'],
                                      })
    else:
        form = QueryForm()
    return render_to_response('query_form.html', {'form': form})

def query(request, queryID):
    if request.session.get('queryLock', False):
        return HttpResponse('Busy, try again later')
    if request.session['queryID'] != queryID:
        raise Http404()


    generateReport(request.session['adID'], request.session['startDate'], request.session['endDate'], request.session['macFormat'], queryID)

    BASEDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp_report')
    filename = os.path.join(BASEDIR, queryID) + '.xls'
    download_name = request.session['adID'] + '.xls' 
    wrapper = FileWrapper(open(filename))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = "attachment; filename= {0}".format(download_name)

    return response
    
    
    





