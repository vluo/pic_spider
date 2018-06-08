import os, sys
import time, random
from urllib import parse
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest

from common import common_func
import my_config.config

class VBase(BaseSpider):
    start_time = 0
    save_path = ''
    finished_album_num = 0
    finished_pic_num = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Origin": "http://www.poco.cn",
        "Referer": "http://www.poco.cn /user/user_center?user_id=173522648",
        "Host": "web-api.poco.cn",
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
        super().__init__()
    #end def

    def close(self):
        logs = []
        logs.append('took ' + str(time.time()-self.start_time) + ' seconds')
        logs.append('finished ' + str(self.finished_album_num) + ' albums')
        logs.append('finished ' + str(self.finished_pic_num)+' pics')
        my_log = "\r\n".join(logs)
        log_file = self._log_file()
        print(log_file)
        common_func.add_log(log_file, my_log)
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

    def _save_pic(self, pic_url, save_path):
        pic_name = pic_url.split('/')[-1]
        pic_path = os.path.join(save_path, pic_name)
        if not os.path.isfile(pic_path):
            import requests
            res = requests.get(pic_url)
            if res and res.status_code == requests.codes.ok:
                print(str(self.finished_pic_num) + ' to save ' + pic_path)
                with open(pic_path, 'wb') as f:
                    f.write(res.content)
                    self.finished_pic_num = self.finished_pic_num + 1
                    # end with
            # end fi
        else:
            print(pic_path + ' exists ')
        # end if
    # end def


    def _save_path(self):
        return os.path.dirname(__file__)
    #end def

#end base