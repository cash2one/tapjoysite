# Create your views here.
# Create your views here.

import uuid, time, re
import os, sys, mimetypes
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from ChangeAMSaleRep.forms import UploadFileForm



def upload_form(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            request.session['queryID'] = query_id = str(uuid.uuid1())
            handle_uploaded_file(request.FILES['filePath'], query_id )
            return HttpResponseRedirect('/change_am/' + query_id)
    else:
        form = UploadFileForm()
    return render(request, 'upload_form.html', {'form': form})


def handle_uploaded_file(f, queryID):
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),'tmp', queryID)
    destination = open(file_name, 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def change_result(request, queryID):
    if request.session['queryID'] != queryID:
        raise Http404()
	
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)),'tmp', queryID)
    file_handle = open(file_name)
    file_lines = file_handle.readlines()
    IDs = [] 
    for file_line in file_lines: 
        partner_id = file_line.strip()
        if not re.search('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', partner_id): 
            raise Http404("A wrong partner_id: " + partner_id) 
        IDs.extend([partner_id])
    file_handle.close() 

    
    return render(request, 'change_result.html', {'IDs': IDs})