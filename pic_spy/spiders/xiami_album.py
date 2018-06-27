import os, sys
import time
import json
import re
from urllib import parse
import random
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.python import to_bytes
from lxml import etree
import my_config.config

from common import VBase
from common import common_func


class TuchongSpider(VBase.VBase):
    name =  'xiami_album'
    start_urls = []
    allowed_domains = ["xiami.com"]
    xiami_cookie = {}
    xiami_headers = {}
    cur_page = 1
    page_size = 20
    finished_pic_num = 0
    finished_album_num = 0
    account_ids = None
    saved_counter = 0
    config = {}

    def __init__(self):
        super().__init__()
        self.config = my_config.config.xiami_config
        self.headers = self._getHeader()
    #end def

    def close(self):
        super().close()
        yield Request(self.config['logout_url'], meta=self.xiami_cookie, method='GET', headers=self.headers)
    #end def

    def start_requests(self):
        #return [self.__login_account()]
        #return self.__parse_song_xml()
        loginUrl = self.config['login_url']
        access_request = Request(loginUrl, callback=self.__login_account, meta={'cookiejar':1}, method='GET', headers=self.headers)

        return [access_request]
    #end def

    def __login_account(self, response):
        #print(response.text)
        initRequests = []
        loginUrl = self.config['login_url']
        postData = {'email': self.config['email'], 'password': self.config['password'], 'remember':'1', 'LoginButton': '登陆'}
        #postData = bytes(json.dumps(postData), encoding='utf-8')
        headers = self.headers  # 'Referer':'http://www.xiami.com/web/login'
        headers['Referer'] = loginUrl
        self.xiami_cookie = {'cookiejar': response.meta['cookiejar']}
        yield FormRequest(loginUrl, callback=self.__crawl_colletion_page, formdata=postData, meta=self.xiami_cookie, method='POST', headers=headers)
        #yield Request(loginUrl, callback=self.__crawl_colletion_page, body=postData, meta={'cookiejar': response.meta['cookiejar']}, method='POST', headers=headers)
    #end def


    def __crawl_colletion_page(self, response):
        #print(response.text)
        #return
        url = self.config['collection_url'].replace('[uid]', self.config['uid'])
        url = url.replace('[page]', '1')
        yield Request(url, callback=self.__parse_collecton_list, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
    #end def

    def __parse_collecton_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        print(response.url)

        next_page = response.css('.all_page .p_redirect_l::attr(href)').extract()
        if len(next_page):
            next_url = next_page[0]
            print('next page:'+next_url)
            host = self._parseHost(response.url)
            yield Request(host+''+next_url, callback=self.__parse_collecton_list, meta={'cookiejar': 1}, method='GET', headers=self.headers)
        #END IF

        #song_name_selector = response.css('.track_list .song_name')#.extract()  #track_list   a:nth-child(1)
        play_btns = response.css('.track_list a.song_toclt::attr(onclick)').extract()
        '''song_names = []
        artist_names = []
        for song_name in song_name_selector:#range(len(play_btns)):
            song_names.append(song_name.css('a::text').extract()[0])
            artist_names.append(song_name.css('.artist_name::text').extract()[0])
        #end if
        '''

        for id in play_btns:
            #print(song_names[i]+'/'+'/'+artist_names[i]+'/'+play_btns[i])
            id = self.__parse_sid(id)
            if self._isDoubleCrawled(id):
                continue
            #end if
            url = self.config['song_info_url'].replace('[sid]', id)
            yield Request(url, callback=self.__parse_song_xml, method='GET', headers=self.headers, meta={'cookiejar': response.meta['cookiejar']})
        #end for

    #end def

    def __parse_sid(self, html):
        html = html.replace("collect('", '')
        return html.replace("');", '')
    #end def


    def __parse_song_xml(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            #self._append_done_list(response.url)
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return
        # end if

        xml = bytes(response.text, encoding='utf-8')#response.text
        try:
            root = etree.XML(xml)
            track = root.find('track')
            if track is None:
                print(response.url+' parse xml failed')
                self._add_log(response.url+' parse xml failed')
                return
            #end if
        except etree.XMLSyntaxError:
            print(response.url+' parse xml failed')
            self._add_log(response.url + ' parse xml failed')
            return
        #end try
        info = {}
        info['song_id'] = track.find('song_id').text
        info['song_name'] = track.find('song_name').text.replace('/', '&')
        info['album_name'] = track.find('album_name').text
        info['album_cover'] = track.find('album_cover').text
        info['artist_name'] = track.find('artist_name').text
        info['location'] = self.__str2url(track.find('location').text)

        if self.__save_song(info):
            self._append_done_list(info['song_id'])
            self.finished_album_names.append(info['artist_name'])
            print(info['location'] + ' done')
        else:
            print(info['location']+' failed')
        #end if
    #end def

    def __save_song(self, info):
        print(info['location'])
        #return
        return self._save_pic(info['location'], self.__save_path(info['artist_name']), info['artist_name']+'_'+info['song_name']+'.mp3')
    #end def

    def __str2url(self, s):
        print(s)
        # s = '9hFaF2FF%_Et%m4F4%538t2i%795E%3pF.265E85.%fnF9742Em33e162_36pA.t6661983%x%6%%74%2i2%22735'
        #4h%2F8an252523F624l3a_%5E8%%%d%9cd7337t3Fm.meFEFEF132%1.%uk335%555553fa55c%tA%1xit79793%8458m3teD%85EEE1Ed21c325p%22i.%%%%%321_E_pFhy156E---7af9ef25E
        #9hFx%33F573yE5E3eft%i237136F%5E-f42t2aF8%7__a38-cfdepFm82566luD6%7482%mi21E8%.t1857fe231.1%395mh5%Ebc1bA2n%219Ep_35-6265%8e2F%363k%E%84b2.tF3268%e5%5c6e
        num_loc = s.find('h')
        rows = int(s[0:num_loc])
        strlen = len(s) - num_loc
        cols = int(strlen / rows)
        right_rows = strlen % rows
        new_s = s[num_loc:]
        output = ''
        for i in range(len(new_s)):
            x = i % rows
            y = i / rows
            p = 0
            if x <= right_rows:
                p = x * (cols + 1) + y
            else:
                p = right_rows * (cols + 1) + (x - right_rows) * cols + y
            output = output+''+new_s[int(p)]
        return parse.unquote(output).replace('^', '0')
    #end def

    def __save_path(self, artist_name):
        #sys.setdefaultencoding("utf-8")
        path = os.path.join(self.save_path, artist_name)
        if not os.path.exists(path):
            os.makedirs(path)
        #end if
        return path
    #end def


#end class

