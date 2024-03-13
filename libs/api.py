# -*- coding: utf-8 -*-
import json
import gzip
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from libs.utils import clientTag, partnerId, get_config_value, log_message

def call_o2_api(url, data):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0', 'Accept-Encoding' : 'gzip', 'Accept' : '*/*', 'Content-type' : 'application/json;charset=UTF-8'} 
    if data != None:
        data = json.dumps(data).encode("utf-8")
    request = Request(url = url , data = data, headers = headers)

    if get_config_value('debug') == 1 or get_config_value('debug') == 'true':
        log_message(str(url))
    if get_config_value('debug') == 1 or get_config_value('debug') == 'true':
        log_message(str(data))
    try:
        response = urlopen(request, timeout = 10)
        if response.getheader("Content-Encoding") == 'gzip':
            gzipFile = gzip.GzipFile(fileobj = response)
            html = gzipFile.read()
        else:
            html = response.read()
        if get_config_value('debug') == 1 or get_config_value('debug') == 'true':
            log_message(str(html))
        if html and len(html) > 0:
            data = json.loads(html)
            return data
        else:
            return []
    except HTTPError as e:
        log_message('Chyba při volání '+ str(url) + ': ' + e.reason)
        return { 'err' : e.reason }  

def o2tv_list_api(post):
    result = []
    fetch = True
    while fetch == True:
        data = call_o2_api(url = 'https://' + partnerId + '.frp1.ott.kaltura.com/api_v3/service/asset/action/list?format=1&clientTag=' + clientTag, data = post)
        if 'err' in data or not 'result' in data or not 'totalCount' in data['result']:
            fetch = False
        else:
            total_count = data['result']['totalCount']
            if total_count > 0:
                for object in data['result']['objects']:
                    result.append(object)
                if total_count == len(result):
                    fetch = False
                else:
                    pager = post['pager']
                    pager['pageIndex'] = pager['pageIndex'] + 1
                    post['pager'] = pager
            else:
                fetch = False
    return result     

