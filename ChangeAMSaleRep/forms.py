#!/usr/bin/env python   
# -*- coding: UTF-8 -*-

import datetime, re
from django.contrib.admin import widgets 
from django import forms
class UploadFileForm(forms.Form):
    filePath = forms.FileField(label = 'Partner id files')
    
    
    
