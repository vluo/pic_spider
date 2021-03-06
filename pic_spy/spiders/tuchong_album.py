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


class TuchongSpider(VBase.VBase):
    name =  'tuchong_album'
    start_urls = []
    allowed_domains = ["tuchong.com", 'photo.tuchong.com']
    api_url = '/rest/2/sites/[uid]/posts?count=[num]&page=1&before_timestamp=0'
    photo_host = 'https://photo.tuchong.com/[uid]/f/[pid].jpg'
    cur_page = 1
    page_size = 20
    finished_pic_num = 0
    finished_album_num = 0
    account_ids = None
    saved_counter = 0
    author_mapping = {}

    def __init__(self):
        super().__init__()
        self.account_ids = my_config.config.artist_list
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            author = id
            if isinstance(self.account_ids[id], list):
                author = self.account_ids[id][1]
                self.account_ids[id] = self.account_ids[id][0]
                self.author_mapping[id] = author
                #print()
            #end if
            save_path = self._save_path(self.account_ids[id], author)
            to_crawl_album_num = 210
            print(save_path)
            if not self._crawlMorePages(save_path):
                to_crawl_album_num = 5
            #end if
            api_url = self.api_url.replace('[num]', str(to_crawl_album_num))
            request = Request(self.account_ids[id]+''+api_url.replace('[uid]', id), callback=self.__parse_alum_list, method='GET', headers=self._getHeader())
            initRequests.append(request)
        #end for
        return initRequests
    #end def

    def __parse_alum_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return None
        # end if
        album_num = 0;
        host = self._parseHost(response.url)
        try:
            jsonObj = json.loads(response.text)
            cur_user_id = 0
            if 'post_list' in jsonObj:
                print(response.url+' >>> to crawl '+str(len(jsonObj['post_list']))+' albums')
                for post in jsonObj['post_list']:
                    post['post_id'] = str(post['post_id'])
                    albumUrl = host + '/rest/posts/' + post['post_id']
                    if self._isDoubleCrawled(albumUrl):
                        break
                    #end if

                    yield Request(albumUrl, callback=self.__parse_album_pics, method='GET', headers=self._getHeader())   #url, callback=None, method='GET', headers=None
                #end for
            else:
                self._add_log('>>>> request api error: <<<<'+response.url)
                print('>>>> request api error: <<<<'+response.url)
            #end if
            if cur_user_id and 'has_more' in jsonObj and jsonObj['has_more']:
                self.cur_page = self.cur_page + 1
                #yield FormRequest(api_url, callback=self.__parse_alum_list, formdata=self.__formData(cur_user_id, self.cur_page), headers=self.headers)
            #end if
        except json.decoder.JSONDecodeError:
            self._add_log(response.url + ' parse json failed')
            print('json error')
        #
    #end def

    def __parse_album_pics(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return None
        # end if
        try:
            jsonObj = json.loads(response.text)
            if 'images' in jsonObj:
                save_path = ''
                newOne = False
                for image in jsonObj['images']:
                    pic_url = self.photo_host.replace('[uid]', str(image['user_id']))
                    pic_url = pic_url.replace('[pid]', str(image['img_id']))
                    author = str(image['user_id'])
                    if author in self.author_mapping:
                        author = self.author_mapping[author]
                    #end if
                    save_path = self.__save_path(response.url, author)
                    if self._save_pic(pic_url, save_path):
                        #self.finished_pic_num = self.finished_pic_num +1
                        newOne = True
                    #end if
                #end for

                if newOne:
                    self._add_daily_log(save_path)
                    self._log_done_album_name(save_path)
                    self._append_done_list(response.url)
                    self.finished_album_num = self.finished_album_num + 1
                #end if
            else:
                self._add_log(response.url + " parse json failed")
                print('>>>  request api error: <<<<<'+response.url)
            #end if
        except json.decoder.JSONDecodeError:
            self._add_log(response.url + " parse json failed")
            print('>>>>json error<<<<<<')
        #
    #end def


    def _save_path(self, url, uid):
        userHost = parse.urlparse(url)[1]
        if userHost == 'tuchong.com':            
            if uid not in self.account_ids:
            	userHost = uid
            else:
            	userHost = uid + '.' + userHost
            #end if
        #end if
        save_path = os.path.join(self.save_path, userHost)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        #end fi
        return save_path
    #end def


#end class

