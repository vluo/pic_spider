import os, sys
import platform
import time, random
import hashlib
from urllib import parse
from scrapy.spiders import Spider
from scrapy.http import FormRequest

from common import common_func
import my_config.config

class VBase(Spider):
    start_time = 0
    save_path = ''
    finished_album_num = 0
    finished_pic_num = 0
    finished_album_names = []
    done_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        #"Origin": "http://www.poco.cn",
        #"Referer": "http://www.poco.cn /user/user_center?user_id=173522648",
        #"Host": "web-api.poco.cn",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
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
        self.start_time = time.time()
        self.save_path = os.path.join(my_config.config.save_path, self.name)
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        # end if
        self.log_path = my_config.config.log_path
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
        # end if
        self._load_done_list()
        super().__init__()
    #end def

    def close(self):
        logs = []
        logs.append('took ' + str(time.time()-self.start_time) + ' seconds')
        logs.append('finished ' + str(self.finished_album_num) + ' albums')
        logs.append('finished ' + str(self.finished_pic_num)+' pics')
        if len(self.finished_album_names):
            logs.append('crawled new pic for album(s) ['+",".join(self.finished_album_names)+']')
        #end if
        my_log = "\r\n".join(logs)
        log_file = self._log_file()
        self._add_log("\r\n["+str(time.strftime('%Y%m%d', time.localtime()))+']'+my_log+"\r\n")
        print(my_log)
        print('>>>>>>>> close here <<<<<<')
    #end def

    def _getHeader(self):
        ua = random.choice(self.user_agent_list)
        if ua:
            self.headers['User-Agent'] = ua
        #end if
        return self.headers
    #end def


    def _add_log(self, lines):
        common_func.add_log(self._log_file(), lines+"\r\n", 'a+')
    #end def

    def _log_file(self):
        dateStr = time.strftime('%Y%m%d', time.localtime())
        return os.path.join(self.log_path, str(dateStr)+'['+self.name+'].log')
    # end def

    def _daily_log_file(self, save_path):
        dateStr = time.strftime('%Y%m%d', time.localtime())
        return os.path.join(save_path, str(dateStr) + '.log')
    #end def

    def _parseHost(self, url):
        segs = parse.urlparse(url)
        return segs[0] + '://' + segs[1]
    #end def

    def _save_pic(self, pic_url, save_path, default_name=''):
        flag = False
        if default_name=='':
            pic_name = pic_url.split('/')[-1]
        else:
            pic_name = default_name
        #end if

        pic_path = os.path.join(save_path, pic_name)
        if not os.path.isfile(pic_path):
            import requests
            res = requests.get(pic_url)
            if res and res.status_code == requests.codes.ok and res.content:
                print(str(self.finished_pic_num) + ' to save ' + pic_path)
                try:
                    with open(pic_path, 'wb') as f:
                        f.write(res.content)
                        self.finished_pic_num = self.finished_pic_num + 1
                        flag = True
                        #end if
                    # end with
                except IOError:
                    print('save '+pic_path+' failed')
                #end try
            else:
                print('request ' + pic_url + ' failed')
            # end fi
        else:
            flag = True
            print(pic_path + ' exists ')
        # end if

        return flag
    # end def


    def _save_path(self):
        return os.path.dirname(__file__)
    #end def

    def _done_list_file(self):
        return os.path.join(self.save_path, 'done-list.log')
    #end def

    def _load_done_list(self):
        doneListFile = self._done_list_file()
        if os.path.exists(doneListFile):
            with open(doneListFile, 'r', encoding='utf-8') as file:
                self.done_list = file.readlines()
                #self.done_list = contents.split("\r\n")
            #end wit
        else:
            print(doneListFile+' not found')
        #end if
    #end def

    def _append_done_list(self, item):
        common_func.add_log(self._done_list_file(), self._md5(item)+"\r\n", 'a+')
    #end def

    def _md5(self, str):
        # 创建md5对象
        hl = hashlib.md5()
        # Tips   此处必须声明encode    若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()
    #end def

    def _sysLineSymbol(self):
        sysstr = platform.system()
        if (sysstr == "Windows"):
            return "\r\n"
        elif (sysstr == "Linux"):
            return "\n"
        else:
            return "\r"
    #end def


    def _isDoubleCrawled(self, url):
        res =  self._md5(url) + self._sysLineSymbol() in self.done_list
        if res:
            print('>>>>crawl [' + url + '] has been done, pass<<<<')
        #end if
        return res
    #end def


    def _log_done_album_name(self, save_path):
        if save_path=='':
            return
        #end def
        save_path = save_path.replace(self.save_path+'/', '')
        if not save_path in self.finished_album_names:#.append()
            self.finished_album_names.append(save_path)
        #end if
    #end def

#end base