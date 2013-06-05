#!/usr/bin/env python   
# -*- coding: UTF-8 -*-

import datetime, re
from django.contrib.admin import widgets 
from django import forms
class QueryForm(forms.Form):
    adID = forms.CharField(required=True, label = 'Campaign ID', max_length = 100) 
    startDate = forms.DateField(required=True, label = 'Start Date')
    endDate = forms.DateField(required=True, label = 'End Date')
    macFormat = forms.ChoiceField(required=True, label = 'Mac Address Format', choices = [('1', u'小写无冒号'),('2', u'大写无冒号'),('3', u'小写有冒号'),('4', u'大写有冒号')])


    def clean_adID(self):
        adID = self.cleaned_data['adID'].strip()
        if not re.search('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', adID): 
            raise forms.ValidationError("Please input correct campaign ID!") 
        return adID 
    
