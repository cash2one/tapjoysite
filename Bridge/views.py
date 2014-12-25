# Create your views here.
import time
import json
import random
import urllib2
import hashlib


from django.http import HttpResponseRedirect, HttpResponse
from Bridge.models import Campaign

from django.shortcuts import get_object_or_404


def jump_snda(request):

    gameid = request.GET('gameid')
    idfa = request.GET('idfa')
    appid = request.GET('appid')
    appkey = request.GET('appkey')
    timestamp = time.time()

    before_sign = 'appid=' + appid + '&gameid=' + gameid + '&idfa=' + idfa +\
        '&timpstamp=' + timestamp + '&appkey=' + appkey

    sign = hashlib.new("md5", before_sign).hexdigest()

def jump_adwo(request):

    a = request.REQUEST.get('idfa')
    idfa = '-'.join([a[:8],a[8:12],a[12:16],a[16:20], a[20:]]).upper()
    advid = request.REQUEST.get('advid')
    pid = request.REQUEST.get('pid')
    keywords = request.REQUEST.get('keywords')
    redirect_url = request.REQUEST.get('redirecturl')

    url = 'http://offer.adwo.com/iofferwallcharge/clk?advid=%s&pid=%s&idfa=%s&keywords=%s' % (
        advid, pid, idfa, keywords)
    res = urllib2.urlopen(url).read()
    return HttpResponseRedirect(redirect_url)

def jump_dianxin(request):
    '''www.tapjoy.cn:8765/channel/dianxin?idfa=TAPJOY_HASHED_ADVERTISING_ID&redirecturl='''
    idfa = request.REQUEST.get('idfa')
    ituneid = request.REQUEST.get('ituneid')
    redirect_url = request.REQUEST.get('redirecturl')

    url = 'http://qb.dianxin.net/iguard/promoted/notify/?adalias=speedkit&source=tapjoy&idfa=%s&appid=%s' % (idfa, ituneid)
    print url
    print redirect_url
    res = urllib2.urlopen(url).read()
    return HttpResponseRedirect(redirect_url)

