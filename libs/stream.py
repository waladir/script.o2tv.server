# -*- coding: utf-8 -*-
import time
from datetime import datetime

from libs.channels import load_channels
from libs.session import load_session
from libs.epg import get_live_epg, get_channel_epg
from libs.api import call_o2_api
from libs.utils import partnerId, get_config_value

def get_channel_id(channel_name):
    channels = load_channels()
    channel_id = -1
    for channel in channels:
        if get_config_value('odstranit_hd') == 1 or get_config_value('odstranit_hd') == 'true': 
            if channels[channel]['name'].replace(' HD', '') == channel_name:
                channel_id = channel                
        else:
            if channels[channel]['name'] == channel_name:
                channel_id = channel
    return channel_id

def get_live(channel_name):
    url = 'http://sledovanietv.sk/download/noAccess-cs.m3u8'
    session = load_session()
    channel_id = get_channel_id(channel_name)
    epg_id = -1
    epg = get_live_epg()[channel_id]
    if 'id' in epg:
        epg_id = epg['id']
    if epg_id > 0:
        post = {"1":{"service":"asset","action":"get","id":epg_id,"assetReferenceType":"epg_internal","ks":session['ks']},"2":{"service":"asset","action":"getPlaybackContext","assetId":epg_id,"assetType":"epg","contextDataParams":{"objectType":"KalturaPlaybackContextOptions","context":"START_OVER","streamerType":"mpegdash","urlType":"DIRECT"},"ks":session['ks']},"apiVersion":"7.8.1","ks":session['ks'],"partnerId":partnerId}    
    else:
        post = {"1":{"service":"asset","action":"get","id":id,"assetReferenceType":"media","ks":session['ks']},"2":{"service":"asset","action":"getPlaybackContext","assetId":id,"assetType":"media","contextDataParams":{"objectType":"KalturaPlaybackContextOptions","context":"PLAYBACK","streamerType":"mpegdash","urlType":"DIRECT"},"ks":session['ks']},"apiVersion":"7.8.1","ks":session['ks'],"partnerId":partnerId}
    try:
        data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/multirequest', data = post)
        if 'err' in data or not 'result' in data or len(data['result']) == 0 or not 'sources' in data['result'][1]:
            if channel_id is not None and 'error' in data['result'][1] and 'message' and data['result'][1]['error'] and data['result'][1]['error']['message'] == 'ProgramStartOverNotEnabled' and post['2']['contextDataParams']['context'] == 'START_OVER':
                post = {"1":{"service":"asset","action":"get","id":channel_id,"assetReferenceType":"media","ks":session['ks']},"2":{"service":"asset","action":"getPlaybackContext","assetId":channel_id,"assetType":"media","contextDataParams":{"objectType":"KalturaPlaybackContextOptions","context":"PLAYBACK","streamerType":"mpegdash","urlType":"DIRECT"},"ks":session['ks']},"apiVersion":"7.8.1","ks":session['ks'],"partnerId":partnerId}
                data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/multirequest', data = post)
        if 'err' not in data and 'result' in data and len(data['result']) > 0 and 'sources' in data['result'][1]:
            urls = {}
            for stream in data['result'][1]['sources']:
                urls.update({stream['type'] : stream['url']})
            if 'DASH' in urls:
                url = urls['DASH']
    except:
        url = 'http://sledovanietv.sk/download/noAccess-cs.m3u8'
    return url

def get_archive(channel_name, start_ts, end_ts):
    url =  "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    start_ts = int(start_ts)
    end_ts = int(end_ts)
    session = load_session()
    channel_id = get_channel_id(channel_name)
    epg = get_channel_epg(id = channel_id, start_ts = start_ts, end_ts = end_ts + 60*60*12)
    if start_ts in epg:
        if epg[start_ts]['endts'] > int(time.mktime(datetime.now().timetuple()))-10:
            return get_live(channel_name)
        else:
            post = {"1":{"service":"asset","action":"get","id":id,"assetReferenceType":"epg_internal","ks":session['ks']},"2":{"service":"asset","action":"getPlaybackContext","assetId":id,"assetType":"epg","contextDataParams":{"objectType":"KalturaPlaybackContextOptions","context":"CATCHUP","streamerType":"mpegdash","urlType":"DIRECT"},"ks":session['ks']},"apiVersion":"7.8.1","ks":session['ks'],"partnerId":partnerId}
            data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/multirequest', data = post)
            if 'err' not in data and 'result' in data and len(data['result']) > 0 and 'sources' in data['result'][1]:
                urls = {}
                for stream in data['result'][1]['sources']:
                    urls.update({stream['type'] : stream['url']})
                if 'DASH' in urls:
                    url = urls['DASH']
            return url
    else:
        return get_live(channel_name)



