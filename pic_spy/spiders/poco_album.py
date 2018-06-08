import os, sys
import time, random
import json
import re
import random
import hashlib

from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector

from common import VBase
from common import common_func
import my_config.config

class PocoSpider(VBase.VBase):
    name =  'poco_album'
    start_urls = []
    allowed_domains = ["poco.cn", 'pocoimg.cn']
    api_url = "http://web-api.poco.cn/v1_1/space/get_user_works_list"
    cur_page = 1
    page_size = 18
    my_poco_id = 173522648
    account_ids = None

    def __init__(self):
        super().__init__()
        self.account_ids = my_config.config.poco_account_ids
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            log_file = self._log_file(self.__save_path(id))
            print (log_file)
            if os.path.exists(log_file):
                print('>>>>crawl [' + id + '] has been done, pass<<<<')
                continue
            else:
                 common_func.add_log(log_file, '')
            # end if

            request = FormRequest(self.api_url, callback=self.__parse_alum_list, formdata=self.__formData(id, self.cur_page), headers=self._getHeader())
            initRequests.append(request)
        #end for
        return initRequests
    #end def

    def __formData(self, uid, page):
        len = self.page_size
        start = (page-1)*len
        param = {"user_id": self.my_poco_id,
                 "visited_user_id": 0,
                 "keyword": "",
                 "year": 0,
                 "length": len,
                 "start": start
                 }
        res = {
            "version": "1.1.0",
            "app_name": "poco_photography_web",
            "os_type": "weixin",
            "is_enc": 0,
            "env": "prod",
            "ctime": int(str(int(time.time())) + "123"),
            "param": None,
            "sign_code": ''
        }
        formdata = {
            'host_port': 'http: // www.poco.cn',
            'req': ''
        }

        header = self.headers
        header['Referer'] = header['Referer'] + "" + str(uid)
        param['visited_user_id'] = int(uid)
        res['param'] = param  # ['visited_user_id'] = id
        res['sign_code'] = self.account_ids[uid]  #self.__sign_code(param)
        formdata['req'] = json.dumps(res)

        return formdata
    #end def


    def __parse_alum_list(self, response):
        if response.status != 200 or response.text == '':
            print(str(response.status) + ' >>>>>>>>> ' + response.text)
            return None
        # end if
        album_num = 0;
        try:
            jsonObj = json.loads(response.text)
            cur_user_id = 0
            if 'data' in jsonObj and 'list' in jsonObj['data']:
                self.finished_album_num = self.finished_album_num + len(jsonObj['data']['list'])
                for work in jsonObj['data']['list']:
                    cur_user_id = int(work['user_id'])
                    #albumUrls.append('http://www.poco.cn/works/detail?works_id='+str(work['works_id']))
                    yield FormRequest('http://www.poco.cn/works/detail?works_id='+str(work['works_id'])+'&['+str(cur_user_id)+']', callback=self.__parse_album)#, formdata=None, headers=self.__getHeader())   #
                    album_num = album_num +1
                #end for
            else:
                print('request api error: '+jsonObj['message'])
            #end if
            if cur_user_id and 'has_more' in jsonObj and jsonObj['has_more']:
                self.cur_page = self.cur_page + 1
                #yield FormRequest(api_url, callback=self.__parse_alum_list, formdata=self.__formData(cur_user_id, self.cur_page), headers=self.headers)
            #end if
        except json.decoder.JSONDecodeError:
            print('json error')
        #
        print (response.url+' >>> to crawl '+str(album_num)+' albums')
    #end def


    def __parse_album(self, response):
        if response.status != 200 or response.text == '':
            print(str(response.status) + ' >>>>>>>>> ' + response.text)
            return None
        # end if

        selector = HtmlXPathSelector(response)
        img_tags = selector.xpath('//img')
        #print(' img tags num: ' + str(len(img_tags)))

        matches = re.search(r'\[(\S+)\]', response.url)
        save_path  = self.save_path
        if matches:
            user_id = matches.group(1)
            save_path = self.__save_path(user_id)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            #end if
        else:
            print('>>>empty user_id<<<<')
            return
        #end if

        for img in img_tags:
            html = img.extract()
            matches = re.search(r'data-src="(\S+)"', html)
            if matches:
                self._save_pic(matches.group(1).replace('//', 'http://'), save_path)
        #end
    #end def


    def __save_path(self, uid):
        return os.path.join(self.save_path, str(uid))
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

