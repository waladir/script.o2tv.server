# -*- coding: utf-8 -*-
import json
import time

from libs.api import o2tv_list_api
from libs.session import load_session
from libs.utils import clientTag, apiVersion, get_config_value, load_json_data, save_json_data

def get_channels():
    channels = {}
    channels_data = {}
    session = load_session()
    post = {"language":"ces","ks":session['ks'],"filter":{"objectType":"KalturaSearchAssetFilter","kSql":"(and asset_type='607' (or entitled_assets='entitledSubscriptions' entitled_assets='free') )"},"pager":{"objectType":"KalturaFilterPager","pageSize":300,"pageIndex":1},"clientTag":clientTag,"apiVersion":apiVersion}
    result = o2tv_list_api(post = post)
    x = 0
    for channel in result:
        if 'ChannelNumber' in channel['metas']:
            number = int(channel['metas']['ChannelNumber']['value'])
        else:
            x += 1
            number = 10000 + x
        if not (get_config_value('ignore_radios') == 'true' and 'tags' in channel and len(channel['tags']) > 0 and 'Genre' in channel['tags'] and len(channel['tags']['Genre']) > 0 and channel['tags']['Genre']['objects'][0]['value'] == 'radio'):
            image = None
            imagesq = None
            if len(channel['images']) > 1:
                for img in channel['images']:
                    if img['ratio'] == '16x9':
                        image = img['url']
                    if img['ratio'] == '2x3':
                        imagesq = img['url'] + '/height/256/width/256'
                if image is None:  
                    image = channel['images'][0]['url'] + '/height/320/width/480'
                if imagesq is None:  
                    imagesq = channel['images'][0]['url'] + '/height/256/width/256'
            else:
                image = None
                imagesq = None
            channels_data.update({int(channel['id']) : {'channel_number' : number, 'o2_number' : number, 'name' : channel['name'].strip(), 'id' : channel['id'], 'logo' : image, 'logosq' : imagesq, 'adult' : channel['metas']['Adult']['value'] , 'visible' : True}})
    for channel in sorted(channels_data, key = lambda channel: channels_data[channel]['channel_number']):
        channels.update({channel : channels_data[channel]})
    return channels

def load_channels(reset = False):
    channels = {}
    if reset == True:
        channels = get_channels()
        save_channels(channels)
        return channels
    data = load_json_data({'filename' : 'channels.txt', 'description' : 'kanálů'})
    if data is not None:
        data = json.loads(data)
        if 'channels' in data and data['channels'] is not None and len(data['channels']) > 0:
            valid_to = int(data['valid_to'])
            channels_data = data['channels']
            for channel in channels_data:
                channels.update({int(channel) : channels_data[channel]})
        else:
            channels = get_channels()
            save_channels(channels)
        if not valid_to or valid_to == -1 or valid_to < int(time.time()):
            channels = get_channels()
            save_channels(channels)
    else:
        channels = get_channels()
        save_channels(channels)
    return channels

def save_channels(channels):
    valid_to = int(time.time()) + 60*60*24
    data = json.dumps({'channels' : channels, 'valid_to' : valid_to})
    save_json_data({'filename' : 'channels.txt', 'description' : 'kanálů'}, data)
