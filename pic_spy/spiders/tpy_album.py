import os, sys
import json
import time
import re
from urllib import parse
import random
import hashlib
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import my_config.config
from common import VBase


class TpySpider(VBase.VBase):
    name =  'tpy_album'
    start_urls = []
    allowed_domains = ["pconline.com.cn"]

    def __init__(self):
        super().__init__()
    #end def

    def start_requests(self):
        initRequests = []
        for url in my_config.config.tpy_blog_urls:
            print('url >>>'+url)
            request = Request(url, callback=self.__parse_alum_list, method='GET', headers=self._getHeader())
            initRequests.append(request)
        #end for
        print(my_config.config.tpy_blog_urls)
        return initRequests
    #end def


    def __parse_alum_list(self, response):
        print('call back>>>>>')
        if response.status != 200 or response.text == '':
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return
        # end if

        matches = re.search(r'(\d+)', response.url)
        if not matches:
            print('uid not found')
            return
        # end if
        uid = matches.group(1)

        albumLinks = response.css('.photo_content li a::attr(href)').extract()
        nextPage = response.css('#JPage .next::attr(href)').extract()
        if nextPage:
            nextLink = self.__userHost(response.url)+''+nextPage[0]
            if not nextLink in my_config.config.tpy_blog_urls:
                yield Request(nextLink, callback=self.__parse_alum_list, method='GET', headers=self._getHeader())
            #end if
            print('news page>>>>'+nextLink)
        else:
            print('no next')
        #end if

        if len(albumLinks):
            for link in albumLinks:
                matches = re.search(r'(\d+)\.html', link)
                if matches:
                    id = matches.group(1)
                    link = link.replace(id, 'list_'+id)
                else :
                    msg = response.url + ' none album'
                    self._add_log(msg)
                    print(msg)
                    continue
                #end if
                link = link+'?uid='+uid
                if self._isDoubleCrawled(link):
                    continue
                #end if
                yield Request(link, callback=self.__parse_album_pics, method='GET', headers=self._getHeader())   #
                #self.finished_album_num = self.finished_album_num + 1
        else:
            msg = response.url+' crawled failed'
            self._add_log(msg)
            print(msg)
        #
    #end def

    def __parse_album_pics(self, response):
        if response.status != 200 or response.text == '':
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return None
        # end if

        matches = re.search(r'uid=(\d+)', response.url)
        if not matches:
            print('uid not found')
            return
        # end if
        uid = matches.group(1)
        save_path = os.path.join(self.save_path, str(uid))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        #end if

        imgLinks = response.css('.aViewHD::attr(oimg)').extract()
        newOne = False
        for link in imgLinks:
            rs = self._save_pic(link, save_path)
            if rs:
                self.finished_pic_num = self.finished_pic_num + 1
                newOne = True
            # end if
        #end for
        self.finished_album_num = self.finished_album_num + 1
        self._append_done_list(response.url)
        if newOne:
            self._log_done_album_name(save_path)
        #end if
    #end def


    def __userHost(self, url):
        segs = parse.urlparse(url)
        return segs[0] + '://' + segs[1]
    #end def


    def __save_pic(self, pic_url, host):
        pic_name =  pic_url.split('/')[-1]
        save_path = os.path.join(self.save_path, host)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # end if
        pic_path = os.path.join(save_path, pic_name)
        if not os.path.isfile(pic_path):
            import requests
            res = requests.get(pic_url)
            if res and res.status_code == requests.codes.ok:
                print('to save '+pic_path)
                try:
                    with open(pic_path, 'wb') as f:
                        f.write(res.content)
                        self.finished_pic_num = self.finished_pic_num+1
                        #print('finished '+str(self.finished_pic_num))
                    #end with
                except IOError:
                    print('save ' +pic_path+' failed')
                    return false
                #end try
            #end fi
        else:
            print(pic_path+' exists ')
            return False
        #end if

        return True
   #end def


#end class

