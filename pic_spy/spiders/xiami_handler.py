import os, sys
import time
import json
import re
from urllib import parse
import random
from pic_spy.spiders import xiami_collection
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.python import to_bytes
from lxml import etree
import my_config.config

from common import VBase
from common import common_func


class xiamiHandler(xiami_collection.xiamiCollectionSpider):
    name = 'xiami_sort_album'
    max_page = 0
    page_counter = 0;
    songs_info = {}

    def __init__(self):
        super().__init__()
    #end def


    def _parse_collecton_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        print(response.url)

        #print(cookie);
        #sys.exit()

        #collection di
        collection_id = 0#response.css('.cdinfo li').extract()
        matches = re.search(r'(\d+)', response.url)
        if matches:
            collection_id = matches.group(1)
        else:
            print('page num not found')
            return
        # end if

        #ajax load
        num_selector = response.css('.cdinfo li').extract()
        matches = re.search(r'(\d+)', num_selector[1])
        if matches:
            num = matches.group(1)
            print('collect song num>>>>>'+num)
            pages = int(int(num)/50)+1
            self.max_page = pages;
            next_page_url = self.collection_config['next_page_url']
            next_page_url = next_page_url.replace('[id]', collection_id)
            org_next_page_url = next_page_url.replace('[page_size]', str(self.collection_config['max_page_size']))
            for i in range(1,pages+1):
                next_page_url = org_next_page_url.replace('[page]', str(i))
                print('next page>>>>>>>>>>>>'+next_page_url)
                yield Request(next_page_url, callback=self._parse_collecton_json_list, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
            #end for
        else:
            print('page num not found')
        #end if

    #end def


    def _parse_collecton_json_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if
        print(response.url)
        try:
            jsonObj = json.loads(response.text)
            if 'result' in jsonObj and len(jsonObj['result']['data'])>0:
                self.page_counter = self.page_counter + 1
                for song in jsonObj['result']['data']:
                    if song['artist_id'] in self.songs_info:
                        self.songs_info[song['artist_id']].append({'id': song['song_id'], 'cid': song['list_id'], 'name':song['name']})
                    else:
                        self.songs_info[song['artist_id']] = [{'id': song['song_id'], 'cid': song['list_id'], 'name':song['name']}]
                    #end if
                #end for
            else:
                pass
            #end if
        except json.decoder.JSONDecodeError:
            self._add_log(' parse json failed ' + str(response.url))
            print(' parse json failed ' + str(response.url))
        #end try


        if self.page_counter == self.max_page:
            cookies = response.request.headers.getlist('Cookie')
            cookie = str(cookies[0]).split(';')[0]
            cookie = cookie.replace("b'_xiamitoken=", '')
            pos = 0
            postData = {
                '_xiamitoken':cookie,
                'list_id':'',
                'order':'',
                'song_id':''
            }
            for info in self.songs_info:
                for song in self.songs_info[info]:
                    postData['song_id'] = str(song['id'])
                    postData['list_id'] = str(song['cid'])
                    postData['order'] = str(pos)
                    pos = pos + 1
                    print(song['name']+' set '+str(pos))
                    yield FormRequest(self.collection_config['set_pos_url'], callback=self.__after_set_position, formdata=postData, meta=self.xiami_cookie, method='POST', headers=self.headers)
                #end for
            #end for
        #end if
    #end def

    def __after_set_position(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        try:
            jsonObj = json.loads(response.text)
            print(jsonObj)
        except json.decoder.JSONDecodeError:
            print(' parse json failed ' + str(response.url))
        #end try
    #end def


#end class

