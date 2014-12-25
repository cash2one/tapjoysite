# Create your views here.
from django.shortcuts import render
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
import os, sys,mimetypes
import json
import calendar
import Qconfig

def chart(request):
    settings = Qconfig.SQL_CONFIG 
    BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'DailyAdSpend','Qreport')
    jsonfile = os.path.join(BASEDIR, 'China' , settings['quarter']) + '.json'

    if os.path.exists(jsonfile):
        f = file(jsonfile)
        spend_data = json.load(f)
        f.close()
    else:
        spend_data = {};

    
    if settings['quarter'] == '2014Q3':
        monthrange = xrange(7, 10)
    if settings['quarter'] == '2014Q4':
        monthrange = xrange(10, 13)
    year = 2014
    
    dates = [] 
    for mon in monthrange:
        for i in xrange(calendar.monthrange(year, mon)[1]):
            dates.append('{0:4d}-{1:02d}-{2:02d}'.format(year, mon, i+1)) 
    
    days = spend_data.keys()
    days.sort();
    
    dat = {};
    # personal kpi sum
    for owner, kpi in settings['kpi'].items():
        dat[owner] = {};
        dat[owner]['QKPI'] = kpi
        dat[owner]['DKPI'] = float(kpi) / settings['days']
        dat[owner]['QtD'] = 0
    
    for i in xrange(0, len(days)):
        daydata = spend_data[days[i]]
        for key, value in daydata.items():
            owner = 'Rae'
            if key in settings['owner']:
                owner = settings['owner'][key]
            dat[owner]['QtD'] += value;
            dat[owner][i] = value + dat[owner].get(i,0);
    
    # total kpi 
    iter = dat.items()
    sum = 'Total'
    dat[sum] = {};
    dat[sum]['QKPI'] = 0
    dat[sum]['DKPI'] = 0
    dat[sum]['QtD'] = 0

    for owner, value in iter:
        dat[sum]['QKPI'] += value['QKPI'];
        dat[sum]['QtD'] += value['QtD'];
        dat[sum]['DKPI'] += value['DKPI'];
        for i in xrange(len(days), 0, -1):
            dat[sum][i-1] = value.get(i-1, 0) + dat[sum].get(i-1, 0)

    daykpi = {}
    dayactual = {}
    pacekpi = {}
    paceactual = {}
    daysum = 0;
    for i in xrange(0, len(dates)):
        pacekpi[dates[i]] = dat[sum]['DKPI']
        daysum += dat[sum]['DKPI']
        daykpi[dates[i]] = daysum;

    daysum = 0
    for i in xrange(0, len(days)):
        paceactual[dates[i]] = dat[sum][i]  
        daysum += dat[sum][i]
        dayactual[dates[i]] = daysum ;

    percent = dayactual[dates[i]] / float(daykpi[dates[len(dates) - 1]]) * 100
  
    
    total = [];
    total.append({u'data':daykpi, u'name': u'target'})
    total.append({u'data':dayactual, u'name': u'actual'})

    totalpacing = []; 
    totalpacing.append({u'data':pacekpi, u'name': u'target'})
    totalpacing.append({u'data':paceactual, u'name': u'actual'})

    data = [];

    data.append({'title':'Total (%.2f%%)' % percent, 'sum':total, 'pace':totalpacing})

    iter = dat.items()

    for owner, value in iter:
        if owner == 'Total':
            continue
        daykpi = {}
	dayactual = {}
	pacekpi = {}
	paceactual = {}
	daysum = 0;
	for i in xrange(0, len(dates)):
	    pacekpi[dates[i]] = dat[owner]['DKPI']
	    daysum += dat[owner]['DKPI']
	    daykpi[dates[i]] = daysum;

	daysum = 0
	for i in xrange(0, len(days)):
            if i not in dat[owner]:  # account change, some accounts change to 0
                dat[owner][i] = 0
	    paceactual[dates[i]] = dat[owner][i]
	    daysum += dat[owner][i]
	    dayactual[dates[i]] = daysum ;
        
        if daykpi[dates[i]] == 0:
	    percent = 0.0
        else:
            percent = dayactual[dates[i]] / float(daykpi[dates[len(dates) - 1]]) * 100
        


	total = [];
	total.append({u'data':daykpi, u'name': u'target'})
	total.append({u'data':dayactual, u'name': u'actual'})

	totalpacing = [];
	totalpacing.append({u'data':pacekpi, u'name': u'target'})
	totalpacing.append({u'data':paceactual, u'name': u'actual'})

	data.append({'title':'%s (%.2f%%)' % (owner, percent), 'sum':total, 'pace':totalpacing})
	   

   
    return render(request, 'DailyAdSpend/charts.html', {'data':data})

   
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
