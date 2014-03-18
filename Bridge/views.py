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


def jump_appdrive(request):
    '''http://211.151.191.4:8765/channel/appdrive?campaign_id=1102&idfa=TAPJOY_ADVERTISING_ID&identifier=d0a951d6-93f5-45f2-ab46-844b44a9b76f'''
    campaign_id = request.REQUEST.get('campaign_id')
    deviceid = request.REQUEST.get('idfa')
    identifier = request.REQUEST.get('identifier')

    idfa = '-'.join(
        [deviceid[:8], deviceid[8:12], deviceid[12:16], deviceid[16:20], deviceid[20:32]]).upper()
    site_id = '1960'
    source = '767'

    sitekey = 'a37c8373f4c87cf782b7618a00c07768'

    redirect_url = 'http://appdriver.cn/6.0.%sac?source=%s&campaign_id=%s&returnFormat=3&idfa=%s&identifier=%s' % (
        site_id, source, campaign_id, idfa, identifier)

    return HttpResponseRedirect(redirect_url)


def postback_appdrive(request):
    '''http://211.151.191.4:8765/channel/appdrive_postback?app_id=89ed3994-eb99-4c00-9788-8279579e0bez&advertising_id=123456994-eb99-4c00-9788-8279579abcez&library_version=server&sdk_type=connect'''
    app_id = request.REQUEST.get('app_id')
    advertising_id = request.REQUEST.get('advertising_id')

    campaign = get_object_or_404(Campaign, app_id=app_id)

    if random.randint(1, 10) <= campaign.campaign_level:
        url = 'https://ws.tapjoyads.com/log_device_app?app_id=%s&advertising_id=%s&library_version=server&sdk_type=connect' % (
            app_id, advertising_id)
        res = urllib2.urlopen(url).read()

        print url
        print res

    json_data = json.dumps({"result": "true"})
    return HttpResponse(json_data, mimetype="application/json", status=200)
