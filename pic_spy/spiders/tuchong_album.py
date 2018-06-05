import os, sys
import json
import time
import re
from urllib import parse
import random
import hashlib
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
import my_config.config


class PocoSpider(BaseSpider):
    name =  'tuchong_album'
    start_urls = []
    allowed_domains = ["tuchong.com", 'photo.tuchong.com']
    api_url = '/rest/2/sites/[uid]/posts?count=100&page=1&before_timestamp=0'
    photo_host = 'https://photo.tuchong.com/[uid]/f/[pid].jpg'
    cur_page = 1
    page_size = 20
    finished_pic_num = 0
    finished_album_num = 0
    account_ids = None
    save_path = '/home/python/pic_spy/albums'
    saved_counter = 0
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Origin":"https://www.tuchong.com",
        "Referer":"https://www.tuchong.com",
        "Connection":"Keep-Alive",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def __init__(self):
        self.save_path = os.path.join(self.save_path, self.name)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # end if
        self.account_ids = my_config.config.artist_list
        super().__init__()
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            request = FormRequest(self.account_ids[id]+''+self.api_url.replace('[uid]', id), callback=self.__parse_alum_list, formdata=None, headers=self.__getHeader())
            initRequests.append(request)
        #end for
        return initRequests
    #end def


    def close(self):
        print('finished ' + str(self.finished_album_num) + ' albums')
        print('finished ' + str(self.finished_pic_num)+' pics')
        print('>>>>>>>> close here <<<<<<')
    #end def


    def __parse_alum_list(self, response):
        if response.status != 200 or response.text == '':
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return None
        # end if
        album_num = 0;
        host = self.__userHost(response.url)
        try:
            jsonObj = json.loads(response.text)
            cur_user_id = 0
            if 'post_list' in jsonObj:
                print(response.url+' >>> to crawl '+str(len(jsonObj['post_list']))+' albums')
                for post in jsonObj['post_list']:
                    yield FormRequest(host+'/rest/posts/'+post['post_id'], callback=self.__parse_album_pics)#, formdata=None, headers=self.__getHeader())   #
                    self.finished_album_num = self.finished_album_num + 1
                #end for
            else:
                print('>>>> request api error: <<<<')
            #end if
            if cur_user_id and 'has_more' in jsonObj and jsonObj['has_more']:
                self.cur_page = self.cur_page + 1
                #yield FormRequest(api_url, callback=self.__parse_alum_list, formdata=self.__formData(cur_user_id, self.cur_page), headers=self.headers)
            #end if
        except json.decoder.JSONDecodeError:
            print('json error')
        #
    #end def

    def __parse_album_pics(self, response):
        if response.status != 200 or response.text == '':
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return None
        # end if
        try:
            jsonObj = json.loads(response.text)
            segs = parse.urlparse(response.url)
            userHost = segs[1]
            if 'images' in jsonObj:
                for image in jsonObj['images']:
                    pic_url = self.photo_host.replace('[uid]', str(image['user_id']))
                    pic_url = pic_url.replace('[pid]', str(image['img_id']))
                    rs = self.__save_pic(pic_url, userHost)
                    if rs:
                        self.finished_pic_num = self.finished_pic_num +1
                    #end if
                #end for
            else:
                print('>>>  request api error: <<<<<')
            #end if
        except json.decoder.JSONDecodeError:
            print('>>>>json error<<<<<<')
        #
    #end def


    def __userHost(self, url):
        segs = parse.urlparse(url)
        return segs[0] + '://' + segs[1]
    #end def

    def __getHeader(self):
        ua = random.choice(self.user_agent_list)
        if ua:
            self.headers['User-Agent'] = ua
        #end if
        return self.headers
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


    def __md5(self, str):
        # 创建md5对象
        hl = hashlib.md5()
        # Tips   此处必须声明encode    若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()
    #end def

    def __sign_code(self, param):
        return 'a2a4d025aa8fe2dbf60'#'841262702a1b4ce4183'
        jsonStr = json.dumps(param);
        jsonStr = self.__md5("poco_" + jsonStr + "_app") #md5
        #    n = n.substr(5, 19);
        return jsonStr[5:24]
    #end def

#end class

