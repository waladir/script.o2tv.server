# -*- coding: utf-8 -*-
import os

import json

clientTag = '9.40.0-PC'
apiVersion = '5.4.0'
partnerId = '3201'

def is_kodi():
    try:
        import xbmc
        test = int(xbmc.getInfoLabel('System.BuildVersion').split('.')[0])
        return True
    except Exception:
        return False

def get_script_path():
    path = os.path.realpath(__file__)
    if path is not None:
        return path.replace('/libs/utils.py', '').replace('\\libs\\utils.py', '')

def get_config_value(setting):
    if is_kodi() == True:
        import xbmcaddon
        addon = xbmcaddon.Addon()
        return addon.getSetting(setting)
    else:
        config_file = os.path.join(get_script_path(), 'config.txt')
        with open(config_file, 'r') as f:
            config = json.load(f)
            f.close()
        if setting in config:
            return config[setting]

def log_message(message):
    if is_kodi() == True:
        import xbmc
        xbmc.log('O2TV Playlist > ' + message) 
    else:
        print(message)

def display_message(message):
    if is_kodi() == True:
        import xbmcgui
        xbmcgui.Dialog().notification('O2TV Playlist', message, xbmcgui.NOTIFICATION_ERROR, 4000)
    else:
        print(message)

def save_json_data(file, data):
    if is_kodi() == True:
        import xbmcaddon
        from xbmcvfs import translatePath
        addon = xbmcaddon.Addon()
        addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    else:
        addon_userdata_dir = os.path.join(get_script_path(), 'data')
    filename = os.path.join(addon_userdata_dir, file['filename'])
    try:
        with open(filename, "w") as f:
            f.write('%s\n' % data)
    except IOError:
        display_message('Chyba uložení ' + file['description'])

def load_json_data(file):
    data = None
    if is_kodi() == True:
        import xbmcaddon
        from xbmcvfs import translatePath
        addon = xbmcaddon.Addon()
        addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    else:
        addon_userdata_dir = os.path.join(get_script_path(), 'data')
    filename = os.path.join(addon_userdata_dir, file['filename'])
    try:
        with open(filename, "r") as f:
            for row in f:
                data = row[:-1]
    except IOError as error:
        if error.errno != 2:
            display_message('Chyba při načtení ' + file['description'])
    return data    

def replace_by_html_entity(string):
    return string.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace("'","&apos;").replace('"',"&quot;")

