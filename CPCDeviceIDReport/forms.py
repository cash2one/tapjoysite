import datetime, re
from django.contrib.admin import widgets 
from django import forms
class QueryForm(forms.Form):
    adID = forms.CharField(required=True, label = 'Campaign ID', max_length = 100) 
    startDate = forms.DateField(required=True, label = 'Start Date')
    endDate = forms.DateField(required=True, label = 'End Date')

    def clean_adID(self):
        adID = self.cleaned_data['adID'].strip()
        if not re.search('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', adID): 
            raise forms.ValidationError("Please input correct campaign ID!") 
        return adID 
    
