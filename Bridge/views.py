# Create your views here.
import time

import hashlib

from django.http import HttpResponseRedirect


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
    '''http://211.151.191.4:8765/channel/appdrive?campaign_id=712&idfa=123456781234456756781234567890ab'''
    campaign_id = request.REQUEST.get('campaign_id')
    deviceid = request.REQUEST.get('idfa')

    idfa = '-'.join(
        [deviceid[:8], deviceid[8:12], deviceid[12:16], deviceid[16:20], deviceid[20:32]]).upper()
    site_id = '1960'
    source = '767'
    sitekey = 'a37c8373f4c87cf782b7618a00c07768'

    redirect_url = 'http://appdriver.cn/6.0.%sac?source=%s&campaign_id=%s&returnFormat=3&idfa=%s' % (
        site_id, source, campaign_id, idfa)

    return HttpResponseRedirect(redirect_url)
