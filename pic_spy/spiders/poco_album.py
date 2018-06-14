import os, sys
import time, random
import json
import re
import random

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
            self.cur_page = 1
            log_file = self._daily_log_file(self.__save_path(id))
            print (log_file)
            if os.path.exists(log_file):
                pass
                #print('>>>>crawl [' + id + '] has been done, pass<<<<')
                #continue
            else:
                 common_func.add_log(log_file, '')
            # end if
            if not isinstance(self.account_ids[id], list):
                self.account_ids[id] = [self.account_ids[id]]
            #end if
            for authCode in self.account_ids[id]:
                request = FormRequest(self.api_url, callback=self.__parse_alum_list, formdata=self.__formData(id, self.cur_page), headers=self._getHeader())
                self.cur_page = self.cur_page + 1
            #end for

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
        header['Referer'] = "http://www.poco.cn/user/user_center?user_id=" + str(uid)
        param['visited_user_id'] = int(uid)
        res['param'] = param  # ['visited_user_id'] = id
        res['sign_code'] = self.account_ids[uid][page-1]  #self.__sign_code(param)
        formdata['req'] = json.dumps(res)

        return formdata
    #end def


    def __parse_alum_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print(str(response.status) + ' >>>>>>>>> ' + response.url)
            return None
        # end if
        album_num = 0;
        try:
            jsonObj = json.loads(response.text)
            cur_user_id = 0
            if 'data' in jsonObj and 'list' in jsonObj['data']:
                for work in jsonObj['data']['list']:
                    cur_user_id = int(work['user_id'])
                    albumUrl = 'http://www.poco.cn/works/detail?works_id='+str(work['works_id'])+'&uid='+str(cur_user_id)
                    if self._isDoubleCrawled(albumUrl):
                        continue
                    # end if

                    yield FormRequest(albumUrl, callback=self.__parse_album)#, formdata=None, headers=self._getHeader())   #
                    album_num = album_num +1
                    self.finished_album_num = self.finished_album_num + len(jsonObj['data']['list'])
                #end for
            else:
                self._add_log(response.url+' parse json failed')
                print('request api error: '+jsonObj['message'])
            #end if
            if cur_user_id and 'has_more' in jsonObj and jsonObj['has_more']:
                self.cur_page = self.cur_page + 1
                #yield FormRequest(api_url, callback=self.__parse_alum_list, formdata=self.__formData(cur_user_id, self.cur_page), headers=self.headers)
            #end if
        except json.decoder.JSONDecodeError:
            self._add_log(response.url + ' parse json failed')
            print('json error')
        #
        print (response.url+' >>> to crawl '+str(album_num)+' albums')
    #end def


    def __parse_album(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed '+str(response.status))
            print(str(response.status) + ' >>>>>>>>> ' + response.url)
            return None
        # end if

        matches = re.search(r'uid=(\S+)', response.url)
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

        self._append_done_list(response.url)

        selector = HtmlXPathSelector(response)
        img_tags = selector.xpath('//img')
        # print(' img tags num: ' + str(len(img_tags)))
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


    def __sign_code(self, param):
        return 'a2a4d025aa8fe2dbf60'#'841262702a1b4ce4183'
        jsonStr = json.dumps(param);
        jsonStr = self.__md5("poco_" + jsonStr + "_app") #md5
        #    n = n.substr(5, 19);
        return jsonStr[5:24]
    #end def

#end class

