import os, sys
import time
import json
import re
from urllib import parse
import random
from pic_spy.spiders import xiami_album
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.python import to_bytes
from lxml import etree
import my_config.config

from common import VBase
from common import common_func


class xiamiCollectionSpider(xiami_album.xiamiSpider):
    name =  'xiami_collection'
    collection_config = {}
    def __init__(self):
        super().__init__()
        self.collection_config = my_config.config.xiami_collection
    #end def


    def _crawl_colletion_page(self, response):
        for url in self.collection_config['list']:
            yield Request(url, callback=self._parse_collecton_list, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
        #end for
    #end def

    def _parse_collecton_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        print(response.url)

        #collection di
        collection_id = 0#response.css('.cdinfo li').extract()
        matches = re.search(r'(\d+)', response.url)
        if matches:
            collection_id = matches.group(1)
        else:
            print('page num not found')
            return
        # end if

        song_name_selector = response.css('.song_name')#.extract()  #track_list   a:nth-child(1)
        song_urls = []
        for song_name in song_name_selector:#range(len(play_btns)):
            song_urls.append(song_name.css('a::attr(href)').extract()[0])
        #end FOR
        #print(song_urls)
        for url in song_urls:
            url = 'https://www.xiami.com'+url
            if self._isDoubleCrawled(url):
                continue
            #end if
            yield Request(url, callback=self._access_song_page, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
        #end for

        #ajax load
        num_selector = response.css('.cdinfo li').extract()
        matches = re.search(r'(\d+)', num_selector[1])
        if matches:
            num = matches.group(1)
            print('collect song num>>>>>'+num)
            pages = int(int(num)/50)+1
            next_page_url = self.collection_config['next_page_url']
            next_page_url = next_page_url.replace('[id]', collection_id)
            org_next_page_url = next_page_url.replace('[page_size]', str(self.collection_config['max_page_size']))
            for i in range(1,pages+1):
                next_page_url = org_next_page_url.replace('[page]', str(i))
                print('next page>>>>>>>>>>>>'+next_page_url)
                yield Request(next_page_url, callback=self.__parse_collecton_json_list, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
            #end for
        else:
            print('page num not found')
        #end if

    #end def


    def _access_song_page(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        self._append_done_list(response.url)

        #do_download
        song_name_selector = response.css('.do_download')  # .extract()  #track_list   a:nth-child(1)
        song_ids = []
        for song_name in song_name_selector:  # range(len(play_btns)):
            song_ids.append(self.__parse_sid(song_name.css('a::attr(onclick)').extract()[0]))
        # end FOR
        #print(song_ids)
        for id in song_ids:
            if self._isDoubleCrawled(id):
                continue
            #end if
            url = self.config['song_info_url'].replace('[sid]', id)
            print(url)
            yield Request(url, callback=self._parse_song_xml, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
        # end for

    #end def

    def _done_list_file(self):
        self.__revisePath()
        print('done list path>>>>>>>>>>'+os.path.join(self.save_path, 'done-list.log'))
        return os.path.join(self.save_path, 'done-list.log')
    #end def

    def __revisePath(self):
        self.save_path = self.save_path.replace(self.name, 'xiami_album')
        if not os.path.exists(self.save_path):
            os.makedirs(path)
        #end if
    #end def


    def __parse_sid(self, html):
        #xm_download('72261', 'song', this);
        html = html.replace("xm_download('", '')
        return html.replace("', 'song', this);", '')
    #end def


    def __parse_collecton_json_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        try:
            jsonObj = json.loads(response.text)
            if 'result' in jsonObj and len(jsonObj['result']['data'])>0:
                for song in jsonObj['result']['data']:
                    if self._isDoubleCrawled(str(song['song_id'])):
                        continue
                    # end if
                    url = self.config['song_info_url'].replace('[sid]', str(song['song_id']))
                    print(url)
                    yield Request(url, callback=self._parse_song_xml, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
                #end for
            else:
                pass
            #end if
        except json.decoder.JSONDecodeError:
            self._add_log(' parse json failed ' + str(response.url))
            print(' parse json failed ' + str(response.url))
        #end try

    #end def



#end class

