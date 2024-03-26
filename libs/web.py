# -*- coding: utf-8 -*-
import os

from urllib.parse import quote, unquote
from bottle import run, route, post, response, request, redirect, template, static_file

from libs.session import load_session
from libs.channels import load_channels
from libs.epg import get_epg, load_epg
from libs.stream import get_live, get_archive
from libs.utils import get_config_value, get_script_path

@route('/epg')
def epg():
    if  int(get_config_value('interval_stahovani_epg')) > 0:
        output = load_epg()
    else:
        output = get_epg()
    response.content_type = 'xml/application; charset=UTF-8'
    return output

@route('/playlist')
def playlist():
    channels = load_channels()
    output = '#EXTM3U\n'
    ip = get_config_value('webserver_ip')
    port = get_config_value('webserver_port')
    for channel in channels:
        if channels[channel]['logo'] == None:
            logo = ''
        else:
            logo =  channels[channel]['logo']
        if get_config_value('odstranit_hd') == 1 or get_config_value('odstranit_hd') == 'true':
            channel_name = channels[channel]['name'].replace(' HD', '')
        else:
            channel_name = channels[channel]['name']
        output += '#EXTINF:-1 provider="O2TV" tvg-chno="' + str(channels[channel]['channel_number']) + '" tvg-logo="' + logo + '" catchup-days="7" catchup="append" catchup-source="?start_ts={utc}&end_ts={utcend}", ' + channel_name + '\n'
        output += '#KODIPROP:inputstream=inputstream.adaptive\n'
        output += '#KODIPROP:inputstream.adaptive.manifest_type=mpd\n'
        output += '#KODIPROP:mimetype=application/dash+xml\n'
        output += 'http://' + str(ip) + ':' + str(port)  + '/play/' + quote(channel_name.replace('/', 'sleš')) + '.mpd\n'
    response.content_type = 'text/plain; charset=UTF-8'
    return output

@route('/play/<channel>')
def play(channel):
    channel = unquote(channel.replace('.mpd', '')).replace('sleš', '/')
    if 'start_ts' in request.query:
        stream = get_archive(channel, request.query['start_ts'], request.query['end_ts'])
    else:
        stream = get_live(channel)
    response.content_type = 'application/dash+xml'
    return redirect(stream)

@route('/img/<image>')
def add_image(image):
    return static_file(image, root = os.path.join(get_script_path(), 'resources', 'templates'))

@route('/')
@post('/')
def page():
    message = ''
    ip = get_config_value('webserver_ip')
    port = get_config_value('webserver_port')
    if request.params.get('action') is not None:
        action = request.params.get('action')
        if action == 'reset_channels':
            load_channels(reset = True)
            message = 'Kanály resetovány!'
        elif action == 'reset_session':
            load_session(reset = True)
            message = 'Sessiona resetována!'
    base_url = 'http://' + str(ip) + ':' + str(port)
    playlist_url = base_url + '/playlist'
    epg_url = base_url + '/epg'
    playlist = []
    channels = load_channels()
    for channel in channels:
        playlist.append({'name' : channels[channel]['name'], 'url' : base_url + '/play/' + quote(channels[channel]['name'].replace('/', 'sleš')) + '.mpd', 'logo' : channels[channel]['logo']})
    return template(os.path.join(get_script_path(), 'resources', 'templates', 'form.tpl'), message = message, playlist_url = playlist_url, epg_url = epg_url, playlist = playlist)

def start_server():
    port = int(get_config_value('webserver_port'))
    run(host = '0.0.0.0', port = port)

