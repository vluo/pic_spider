import os, sys
import json
import time
import re
import hashlib
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest

class PocoSpider(BaseSpider):
    name =  'poco_album_spider'
    start_urls = []
    allowed_domains = ["poco.cn", 'pocoimg.cn']
    api_url = "http://web-api.poco.cn/v1_1/space/get_user_works_list"
    cur_page = 1
    page_size = 18
    my_poco_id = 173522648
    account_ids = [178392616]
    save_path = '/home/python/pic_spy/albums'
    saved_counter = 0
    headers={
        "User - Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Origin":"http: // www.poco.cn",
        "Referer":"http: // www.poco.cn / user / user_center?user_id =",
        "Host":"web-api.poco.cn",
        "Connection":"Keep-Alive",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }

    def __init__(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # end if
        super().__init__()
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            request = FormRequest(self.api_url, callback=self.__parse_alum_list, formdata=self.__formData(id, self.cur_page), headers=self.headers)
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
        param['visited_user_id'] = uid
        res['param'] = param  # ['visited_user_id'] = id
        res['sign_code'] = self.__sign_code(param)
        formdata['req'] = json.dumps(res)

        print(formdata)

        return formdata
    #end def


    def __parse_alum_list(self, response):
        albumUrls = []
        try:
            jsonObj = json.loads(response.text)
            cur_user_id = 0
            if 'data' in jsonObj and 'list' in jsonObj['data']:
                for work in jsonObj['data']['list']:
                    cur_user_id = int(work['user_id'])
                    #albumUrls.append('http://www.poco.cn/works/detail?works_id='+str(work['works_id']))
                    yield FormRequest('http://www.poco.cn/works/detail?works_id='+str(work['works_id']), callback=self.__parse_album)
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
        print(albumUrls)
    #end def

    def __parse_album(self, response):
        selector = HtmlXPathSelector(response)
        img_tags = selector.select('//img')
        for img in img_tags:
            html = img.extract()
            matches = re.search(r'data-src="(\S+)"', html)
            if matches:
                self.__save_pic(matches.group(1).replace('//', 'http://'))
        #end
    #end def

    def __save_pic(self, pic_url):
        pic_name =  pic_url.split('/')[-1]
        pic_path = os.path.join(self.save_path, pic_name)
        if not os.path.isfile(pic_path):
            import requests
            res = requests.get(pic_url)
            if res and res.status_code == requests.codes.ok:
                print('to save '+pic_path)
                with open(pic_path, 'wb') as f:
                    f.write(res.content)
                    self.saved_counter = self.saved_counter+1
                    print('finished '+str(self.saved_counter))
                #end with
            #end fi
        else:
            print(pic_path+' exists ')
        #end if
   #end def


    def parse(self, response):
        selector = HtmlXPathSelector(response)
        title = selector.select('/html/head/title/text()')
        print('title='+title.extract()[0])
    #end def


    def __md5(self, str):
        # 创建md5对象
        hl = hashlib.md5()
        # Tips
        # 此处必须声明encode
        # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
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

