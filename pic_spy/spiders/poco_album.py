import os, sys
import json
import time
import re
import random
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
    account_ids = {
    	'174574302':'f2a37d9659d2fb48085',
    	'174572931':'406ef59705efb4e425f',
    	'177176218':'9229061252cccadb18f',
    	'173388816':'6b5b2f8292b593118ad',
    	'174848104':'3e1daaec63f772edfcc',
    	'185652848':'8e39023858be8d32e21',
    	'200513958':'77c2259120872addd25',
    	'63443172':'35aa80b13d3ad3d5d4e',
    	'178957211':'5575cdfba172fd87a46',
    	'174079515':'3f24a5c860313797d4d',
    	'19430718':'0ce08eed59bd0cef426',
    	'67593620':'054a8f14068e0c51998',
    	'3417570':'ced79f0568fa7cadaa1',
    	'174730832':'90d1fe0c81a11a1f17c',
    	'66546564':'1177c50fe7622b99154'
    }
    save_path = '/home/python/pic_spy/albums'
    saved_counter = 0
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Origin":"http://www.poco.cn",
        "Referer":"http://www.poco.cn /user/user_center?user_id=173522648",
        "Host":"web-api.poco.cn",
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
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # end if
        super().__init__()
    #end def

    def start_requests(self):
        initRequests = []
        for id in self.account_ids:
            request = FormRequest(self.api_url, callback=self.__parse_alum_list, formdata=self.__formData(id, self.cur_page), headers=self.__getHeader())
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
                for work in jsonObj['data']['list']:
                    cur_user_id = int(work['user_id'])
                    #albumUrls.append('http://www.poco.cn/works/detail?works_id='+str(work['works_id']))
                    yield FormRequest('http://www.poco.cn/works/detail?works_id='+str(work['works_id']), callback=self.__parse_album)#, formdata=None, headers=self.__getHeader())   #
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
        print (' to crawl '+str(album_num)+' albums')
    #end def

    def __getHeader(self):
        ua = random.choice(self.user_agent_list)
        if ua:
            self.headers['User-Agent'] = ua
        #end if
        return self.headers
    #end def

    def __parse_album(self, response):
        if response.status != 200 or response.text == '':
            print(str(response.status) + ' >>>>>>>>> ' + response.text)
            return None
        # end if

        selector = HtmlXPathSelector(response)
        img_tags = selector.xpath('//img')
        #print(' img tags num: ' + str(len(img_tags)))

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

