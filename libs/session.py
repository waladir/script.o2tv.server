# -*- coding: utf-8 -*-
import sys

import json
import time

from libs.api import call_o2_api
from libs.utils import clientTag, partnerId, apiVersion, get_config_value, display_message, load_json_data, save_json_data

def get_token():
    session_data = {}
    post = {'language' : '*', 'partnerId' : int(partnerId), 'clientTag' : clientTag, 'apiVersion' : apiVersion}
    data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/ottuser/action/anonymousLogin?format=1&clientTag=' + clientTag, data = post)
    if 'err' in data or not 'result' in data or not 'objectType' in data['result'] or data['result']['objectType'] != 'KalturaLoginSession':
        display_message('Problém při přihlášení')
        sys.exit() 
    ks = data['result']['ks']

    post = {'username' : get_config_value('username'), 'password' : get_config_value('password'), 'udid' : get_config_value('deviceid'), 'service' : 'https://www.new-o2tv.cz/'} 
    data = call_o2_api(url = 'https://login-a-moje.o2.cz/cas-external/v1/login', data = post)
    if 'err' in data or not 'jwt' in data or not 'refresh_token' in data:
        display_message('Chyba při přihlášení, zkontrolujte jméno a heslo')
        sys.exit() 
    jwt_token = data['jwt']

    post = {"intent":"Service List","adapterData":[{"_allowedEmptyArray":[],"_allowedEmptyObject":[],"_dependentProperties":{},"key":"access_token","value":jwt_token,"relatedObjects":{}},{"_allowedEmptyArray":[],"_allowedEmptyObject":[],"_dependentProperties":{},"key":"pageIndex","value":"0","relatedObjects":{}},{"_allowedEmptyArray":[],"_allowedEmptyObject":[],"_dependentProperties":{},"key":"pageSize","value":"100","relatedObjects":{}}],"ks":ks}
    data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api/p/' + partnerId + '/service/CZ/action/Invoke', data = post)
    if 'err' in data or not 'result' in data or not 'adapterData' in data['result'] or not 'service_list' in data['result']['adapterData']:
        display_message('Problém při přihlášení')
        sys.exit() 
    services = json.loads(data['result']['adapterData']['service_list']['value'])

    services = services['ServicesList']
    ks_codes = {}
    ks_names = {}
    for service in services:
        for id in service:
            ks_codes.update({service[id] : service[id]})
            ks_names.update({service[id] : id})

    if len(ks_codes) < 1:
        display_message('Problém při přihlášení')
        sys.exit() 
    idx = 1
    if get_config_value('poradi_sluzby') is None:
        service_index = -1
    else:
        service_index = int(get_config_value('poradi_sluzby'))
        if service_index > len(ks_codes):
            service_index = -1
    
    for service in ks_codes:
        post = {'language' : 'ces', 'ks' : ks, 'partnerId' : int(partnerId), 'username' : 'NONE', 'password' : 'NONE', 'extraParams' : {'token' : {'objectType' : 'KalturaStringValue', 'value' : jwt_token}, 'loginType' : {'objectType' : 'KalturaStringValue', 'value' : 'accessToken'}, 'brandId' : {'objectType' : 'KalturaStringValue', 'value' : '22'}, 'externalId' : {'objectType' : 'KalturaStringValue', 'value' : ks_codes[service]}}, 'udid' : get_config_value('deviceid'), 'clientTag' : clientTag, 'apiVersion' : apiVersion}
        data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/ottuser/action/login?format=1&clientTag=' + clientTag, data = post)
        if 'err' in data or not 'result' in data or not 'objectType' in data['result'] or data['result']['objectType'] != 'KalturaLoginResponse' or not 'loginSession' in data['result']:
            display_message('Problém při přihlášení')
            sys.exit() 
        session_data.update({'ks_name' : ks_names[service], 'ks_code' : ks_codes[service], 'ks_expiry' : data['result']['loginSession']['expiry'], 'ks_refresh_token' : data['result']['loginSession']['refreshToken'], 'ks' : data['result']['loginSession']['ks']})
        if service_index > 0 and idx == service_index:
            return session_data
        idx = idx + 1
    return session_data

def load_session(reset = False):
    if reset == True:
        session_data = get_token()
        save_session(session_data)
        return session_data
    data = load_json_data({'filename' : 'session.txt', 'description' : 'session'})
    if data is not None:
        data = json.loads(data)
        if 'session_data' in data:
            session_data = data['session_data']
            if 'ks_expiry' not in session_data or int(session_data['ks_expiry']) < int(time.time()):
                session_data = get_token()
                save_session(session_data)
        else:
            session_data = get_token()
            save_session(session_data)
    else:
        session_data = get_token()
        save_session(session_data)
    return session_data

def save_session(session_data):
    data = json.dumps({'session_data' : session_data})        
    save_json_data({'filename' : 'session.txt', 'description' : 'session'}, data)


