# -*- coding: utf-8 -*-
import json
import time
from datetime import datetime

from libs.api import o2tv_list_api
from libs.session import load_session
from libs.channels import load_channels
from libs.utils import clientTag, apiVersion, replace_by_html_entity, get_config_value, display_message, save_json_data, load_json_data

def get_live_epg():
    session = load_session()
    current_timestamp = int(time.time())
    post = {"language":"ces","ks":session['ks'],"filter":{"objectType":"KalturaSearchAssetFilter","orderBy":"START_DATE_ASC","kSql":"(and start_date <= '" + str(current_timestamp) + "' end_date  >= '" + str(current_timestamp) + "' asset_type='epg' auto_fill= true)"},"pager":{"objectType":"KalturaFilterPager","pageSize":500,"pageIndex":1},"clientTag":clientTag,"apiVersion":apiVersion}
    return epg_api(post = post, key = 'channel_id')

def get_channel_epg(id, start_ts, end_ts):
    session = load_session()
    post = {"language":"ces","ks":session['ks'],"filter":{"objectType":"KalturaSearchAssetFilter","orderBy":"START_DATE_ASC","kSql":"(and linear_media_id:'" + str(id) + "' start_date >= '" + str(start_ts) + "' start_date  <= '" + str(end_ts) + "' asset_type='epg' auto_fill= true)"},"pager":{"objectType":"KalturaFilterPager","pageSize":500,"pageIndex":1},"clientTag":clientTag,"apiVersion":apiVersion}
    return epg_api(post = post, key = 'startts')

def epg_api(post, key):
    epg = {}
    result = o2tv_list_api(post = post)
    for item in result:
        if (item['objectType'] == 'KalturaProgramAsset' or item['objectType'] == 'KalturaRecordingAsset') and 'linearAssetId' in item:
            id = item['id']
            channel_id = item['linearAssetId']
            title = item['name']
            if 'description' in item:
                description = item['description']
            else:
                description = ''
            startts = item['startDate']
            endts = item['endDate']

            cover = ''
            poster = ''
            imdb = ''
            year = ''
            contentType = ''
            original = ''
            genres = []
            cast = []
            directors = []
            writers = []
            country = ''

            ratios = {'2x3' : '/height/720/width/480', '3x2' : '/height/480/width/720', '16x9' : '/height/480/width/853'}
            if len(item['images']) > 0:
                poster = item['images'][0]['url'] + ratios[item['images'][0]['ratio']]
            if len(item['images']) > 1:
                cover = item['images'][1]['url'] + ratios[item['images'][1]['ratio']]
            if 'original_name' in item['metas']:
                original = item['metas']['original_name']['value']
            if 'imdb_id' in item['metas']:
                imdb = str(item['metas']['imdb_id']['value'])
            if 'Year' in item['metas']:
                year = str(item['metas']['Year']['value'])
            if 'ContentType' in item['metas']:
                contentType = item['metas']['ContentType']['value']
            if 'Genre' in item['tags']:
                for genre in item['tags']['Genre']['objects']:
                    genres.append(genre['value'])
            if 'PersonReference' in item['tags']:
                for person in item['tags']['PersonReference']['objects']:
                    person_data = person['value'].split('|')
                    if len(person_data) < 3:
                        person_data.append('')
                    cast.append((person_data[1], person_data[2]))
            if 'Director' in item['tags']:
                for director in item['tags']['Director']['objects']:
                    directors.append(director['value'])
            if 'Writers' in item['tags']:
                for writer in item['tags']['Writers']['objects']:
                    writers.append(writer['value'])
            if 'Country' in item['tags'] and 'value' in item['tags']['Country']:
                country = item['tags']['Country']['value']

            episodeNumber = -1
            seasonNumber = -1
            episodesInSeason = -1
            episodeName = ''
            seasonName = ''
            seriesName = ''    

            if 'EpisodeNumber' in item['metas']:
                episodeNumber = int(item['metas']['EpisodeNumber']['value'])
                if episodeNumber > 0:
                    title = title + ' (' + str(episodeNumber) + ')'
            if 'SeasonNumber' in item['metas']:
                seasonNumber = int(item['metas']['SeasonNumber']['value'])
            if 'EpisodeInSeason' in item['metas']:
                episodesInSeason = int(item['metas']['EpisodeInSeason']['value'])
            if 'EpisodeName' in item['metas']:
                episodeName = str(item['metas']['EpisodeName']['value'])
            if 'SeasonName' in item['metas']:
                seasonName = str(item['metas']['SeasonName']['value'])
            if 'SeriesName' in item['metas']:
                seriesName = str(item['metas']['SeriesName']['value'])
            if 'IsSeries' in item['metas'] and int(item['metas']['IsSeries']['value']) == 1:
                isSeries = True
                if 'SeriesID' in item['metas']:
                    seriesId = item['metas']['SeriesID']['value']
                else:
                    seriesId = ''
            else:
                isSeries = False
                seriesId = ''

            md = None
            md_ids = []

            epg_item = {'id' : id, 'title' : title, 'channel_id' : channel_id, 'description' : description, 'startts' : startts, 'endts' : endts, 'cover' : cover, 'poster' : poster, 'original' : original, 'imdb' : imdb, 'year' : year, 'contentType' : contentType, 'genres' : genres, 'cast' : cast, 'directors' : directors, 'writers' : writers, 'country' : country, 'episodeNumber' : episodeNumber, 'seasonNumber' : seasonNumber, 'episodesInSeason' : episodesInSeason, 'episodeName' : episodeName, 'seasonName' : seasonName, 'seriesName' : seriesName, 'isSeries' : isSeries, 'seriesId' : seriesId, 'md' : md, 'md_ids' : md_ids}
            if key == 'startts':
                epg.update({int(str(channel_id) + str(startts)) : epg_item})
            elif key == 'channel_id':
                epg.update({channel_id : epg_item})
            elif key == 'id':
                epg.update({id : epg_item})
    return epg

def get_epg():
    tz_offset = int((time.mktime(datetime.now().timetuple())-time.mktime(datetime.utcnow().timetuple()))/3600)
    channels = load_channels()
    output = ''
    if len(channels) > 0:
        try:
            output = '<?xml version="1.0" encoding="UTF-8"?>\n'
            output += '<tv generator-info-name="EPG grabber">\n'
            for id in channels:
                logo = channels[id]['logo']
                if logo is None:
                    logo = ''
                if get_config_value('odstranit_hd') == 1 or get_config_value('odstranit_hd') == 'true':
                    channel_name = channels[id]['name'].replace(' HD', '')
                else:
                    channel_name = channels[id]['name']
                output += '    <channel id="' + replace_by_html_entity(channel_name) + '">\n'
                output += '            <display-name lang="cs">' +  replace_by_html_entity(channel_name) + '</display-name>\n'
                output += '            <icon src="' + logo + '" />\n'
                output += '    </channel>\n'

            today_date = datetime.today() 
            today_start_ts = int(time.mktime(datetime(today_date.year, today_date.month, today_date.day) .timetuple()))
            today_end_ts = today_start_ts + 60*60*24 - 1

            session = load_session()
            channels_ids = []
            for id in channels:
                channels_ids.append("linear_media_id:'" + str(id) + "'")
            for i in range(0, len(channels_ids), 5):
                channels_query = ' '.join(channels_ids[i:i+5])
                cnt = 0
                content = ''
                post = {"language":"ces","ks":session['ks'],"filter":{"objectType":"KalturaSearchAssetFilter","orderBy":"START_DATE_ASC","kSql":"(and (or " + channels_query + ") start_date >= '" + str(today_start_ts - 60*60*24*int(get_config_value('epg_dnu_zpetne'))) + "' end_date  <= '" + str(today_end_ts + 60*60*24*int(get_config_value('epg_dnu_dopredu'))) + "' asset_type='epg' auto_fill= true)"},"pager":{"objectType":"KalturaFilterPager","pageSize":500,"pageIndex":1},"clientTag":clientTag,"apiVersion":apiVersion}
                epg =  epg_api(post = post, key = 'startts')
                for ts in sorted(epg.keys()):
                    epg_item = epg[ts]
                    starttime = datetime.fromtimestamp(epg_item['startts']).strftime('%Y%m%d%H%M%S')
                    endtime = datetime.fromtimestamp(epg_item['endts']).strftime('%Y%m%d%H%M%S')
                    if get_config_value('odstranit_hd') == 1 or get_config_value('odstranit_hd') == 'true':
                        channel_name = channels[epg_item['channel_id']]['name'].replace(' HD', '')
                    else:
                        channel_name = channels[epg_item['channel_id']]['name']
                    content = content + '    <programme start="' + starttime + ' +0' + str(tz_offset) + '00" stop="' + endtime + ' +0' + str(tz_offset) + '00" channel="' +  replace_by_html_entity(channel_name) + '">\n'
                    content = content + '       <title>' +  replace_by_html_entity(epg_item['title']) + '</title>\n'
                    # content = content + '       <title lang="cs">' +  replace_by_html_entity(epg_item['title']) + '</title>\n'
                    # if epg_item['original'] != None and len(epg_item['original']) > 0:
                    #     content = content + '       <title>' +  replace_by_html_entity(epg_item['original']) + '</title>\n'
                    if epg_item['description'] != None and len(epg_item['description']) > 0:
                        content = content + '       <desc lang="cs">' +  replace_by_html_entity(epg_item['description']) + '</desc>\n'
                    if epg_item['episodeName'] != None and len(epg_item['episodeName']) > 0:
                        content = content + '       <sub-title lang="cs">' +  replace_by_html_entity(epg_item['episodeName']) + '</sub-title>\n'
                    if epg_item['episodeNumber'] != None and epg_item['seasonNumber'] != None and epg_item['episodeNumber'] > 0 and epg_item['seasonNumber'] > 0:
                        if epg_item['episodesInSeason'] != None and epg_item['episodesInSeason'] > 0:
                            content = content + '       <episode-num system="xmltv_ns">' + str(epg_item['seasonNumber']-1) + '.' + str(epg_item['episodeNumber']-1) + '/' + str(epg_item['episodesInSeason']) + '.0/0"</episode-num>\n'
                        else:
                            content = content + '       <episode-num system="xmltv_ns">' + str(epg_item['seasonNumber']-1) + '.' + str(epg_item['episodeNumber']-1) + '.0/0"</episode-num>\n'
                    content = content + '       <icon src="' + epg_item['poster'] + '"/>\n'
                    content = content + '       <credits>\n'
                    for person in epg_item['cast']: 
                        content = content + '         <actor role="' +  replace_by_html_entity(person[1]) + '">' +  replace_by_html_entity(person[0]) + '</actor>\n'
                    for director in epg_item['directors']: 
                        content = content + '         <director>' +  replace_by_html_entity(director) + '</director>\n'
                    content = content + '       </credits>\n'
                    for category in epg_item['genres']:
                        content = content + '       <category>' +  replace_by_html_entity(category) + '</category>\n'
                    if len(str(epg_item['year'])) > 0 and int(epg_item['year']) > 0:
                        content = content + '       <date>' + str(epg_item['year']) + '</date>\n'
                    if len(epg_item['country']) > 0:
                        content = content + '       <country>' +  replace_by_html_entity(epg_item['country']) + '</country>\n'
                    content = content + '    </programme>\n'
                    cnt = cnt + 1
                    if cnt > 20:
                        output += content
                        content = ''
                        cnt = 0
                output += content
            output += '</tv>\n'
        except Exception:
            display_message('Chyba při stahování EPG!')
    return output

def load_epg(reset = False):
    epg = ''
    if reset == True:
        epg = get_epg()
        save_epg(epg)
        return epg
    data = load_json_data({'filename' : 'epg.txt', 'description' : 'EPG'})
    if data is not None:
        data = json.loads(data)
        if 'epg' in data and len(data['epg']) > 0:
            return data['epg']
        else:
            epg = get_epg()
            save_epg(epg)
    else:
        epg = get_epg()
        save_epg(epg)
    return epg

def save_epg(epg):
    data = json.dumps({'epg' : epg})
    save_json_data({'filename' : 'epg.txt', 'description' : 'EPG'}, data)
