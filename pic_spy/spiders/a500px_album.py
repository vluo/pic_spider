# -*- coding: utf-8 -*-
import os, sys
import time
import json
import re
from urllib import parse
import random
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import my_config.config

from common import VBase
from common import common_func


class A500pxAlbumSpider(VBase.VBase):
    name = '500px_album'
    allowed_domains = ['500px.com']
    account_ids = []

    def __init__(self):
        super().__init__()
        self.account_ids = my_config.config.five_hundred_artist_list
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            save_path = self.__save_path(id)
            log_file = self._daily_log_file(save_path)
            if os.path.exists(log_file):
                pass
                #print('>>>>crawl ['+self.account_ids[id]+'] has been done, pass<<<<')
                #continue
            else:
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
            # end if

            request = Request(id+'?ftid='+str(self.account_ids.index(id)), callback=self.__parse_pic_url, method='GET', headers=self._getHeader())
            initRequests.append(request)
        #end for
        return initRequests
    #end def

    def __parse_pic_url(self, response):
        js = response.css('#bootstrap_data').extract()[0]
        jsonStr = js.split("\n")[-2]
        jsonStr = jsonStr.replace('App.bootstrap = ', '')

        matches = re.search(r'ftid=(.*)', response.url)
        if matches:
            save_path = self.__save_path(self.account_ids[int(matches.group(1))])
        else:
            print('url id not found')
            return
        #end if

        #save_path = os.path.join(self.save_path, string(id))
        try:
            jsonObj = json.loads(jsonStr)
            if 'userdata' in jsonObj and 'photos' in jsonObj['userdata']:
                for photo in jsonObj['userdata']['photos']:
                    imgUrl = photo['image_url'][-1]
                    if not self._isDoubleCrawled(imgUrl):
                        if self._save_pic(imgUrl, save_path, self._md5(imgUrl)+'.jpg'):
                            self._append_done_list(imgUrl)
                        #end if
                    #end if
                #end for
            #end if
        except json.decoder.JSONDecodeError:
            print('json error')
        #end try
    #end def


    def __secondDir(self, url):
        return  url.split('/')[-1]#parse.urlparse(url)[1]
    #end def

    def __save_path(self, url):
        userHost = self.__secondDir(url)+'.500px.com'
        return os.path.join(self.save_path, userHost)
    #end def

    #end def
#end class
