import os, sys
import time, random
import json
import re
import random

from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from common import VBase
from common import common_func
import my_config.config

class LofterSpider(VBase.VBase):
    name =  'lofter_album'
    start_urls = []
    allowed_domains = ['lofter.com']
    blogs = {}
    blogs_arr = []
    blog_cookies = {}
    header = None
    post_num = {}

    def __init__(self):
        super().__init__()
        self.blogs = my_config.config.lofter_blogs
    #end def

    def start_requests(self):
        self.header = self._getHeader()
        requests = []
        entryUrl = 'http://www.lofter.com/userentry.do?target={}/view'
        for blog in self.blogs:
            #formdata=postData, meta=self.xiami_cookie, method='POST', headers=headers
            blog = blog['home']
            self.blogs_arr.append(blog)
            self.header['Referer'] = blog
            yield Request(entryUrl.format(blog), callback=self.__call_blog_api, method='GET', headers=self.header, meta={'cookiejar':1})
            #yield Request(blog + '/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr?pos=' + str(self.blogs.index(blog)), callback=self.__parse_post_list, method='POST', headers=self.header, meta={'cookiejar': response.meta['cookiejar']})
        # end for

        return requests
    #end def


    def __call_blog_api(self, response):
        print('after blog list >>>>>>>>>>>>>>>>> ' + response.url)
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print(str(response.status) + ' >>>>>>>>> ' + response.url)
            return
        # end if

        blog = self._parseHost(response.url)

        blog_html = response.css('#control_frame::attr(src)').extract()
        matches = re.search('blogId=(\d+)', blog_html[0])
        if matches:
            blog_id = matches.group(1)
        else:
            print(response.url+' no blog id found')
            return
        #end if
        post_num = (200 if self._crawlMorePages(self.__save_path(blog)) else 5)
        print('to craw %4d '%post_num+' posts of '+blog)
        post_data = {
            'callCount':'1',
            'scriptSessionId':'${scriptSessionId}187',
            'httpSessionId':'',
            'c0-scriptName':'ArchiveBean',
            'c0-methodName':'getArchivePostByTime',
            'c0-id':'0',
            'c0-param0':'boolean:false',
            'c0-param1':'number:'+str(blog_id),#blog id
            'c0-param2':'number:1533000287367',
            'c0-param3':'number:'+str(post_num),
            'c0-param4':'boolean:false',
            'batchId':'604545'
        }
        #formdata=postData, meta=self.xiami_cookie, method='POST', headers=headers
        self.header['Referer'] = blog
        print('call api >>>'+blog + '/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr')
        yield FormRequest(
            blog + '/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr',
            callback=self.__parse_post_list, formdata=post_data, method='POST', headers=self.header,
            meta={'cookiejar': response.meta['cookiejar']})
        #yield Request(blog + '/dwr/call/plaincall/ArchiveBean.getArchivePostByTime.dwr?pos=' + str(self.blogs.index(blog)), callback=self.__parse_post_list, method='POST', headers=self.header, meta={'cookiejar': response.meta['cookiejar']})

    #end def


    def __parse_post_list(self, response):
        print('to parse post list')
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print(str(response.status) + ' >>>>>>>>> ' + response.url)
            return
        # end if

        blog_link = 'http://'+self._parseDomian(response.url)

        post_ids = re.findall('permalink="(.*?)"', response.text)
        if not post_ids:
            self._add_log('not post id found >>>>>>> ' + response.text)
            print('not post id found')
        #end if

        self.header['Referer'] = blog_link
        for id in post_ids:
            link = blog_link+'/post/'+id
            if blog_link in self.post_num: # = self.post_num +1
                self.post_num[blog_link] = self.post_num[blog_link] + 1
            else:
                self.post_num[blog_link] = 1
            #end if
            print('post %04d '%self.post_num[blog_link]+' in : '+blog_link)
            if not self._isDoubleCrawled(link):
                print('to crawl >>>'+link)
                yield Request(link, callback=self.__parse_post_content, method='GET', headers=self.header)
            else:
                break
            #end if
        # end if
    #end def


    def __parse_post_content(self, response):
        #postinner pic img:src
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed '+str(response.status))
            print(str(response.status) + ' >>>>>>>>> ' + response.url)
            return None
        # end if

        blog_link = 'http://'+self._parseDomian(response.url)

        save_path = self.__save_path(blog_link)
        if save_path is None:
            print('create path for '+blog_link+' failed')
            return
        #end if

        pattern = ''
        if blog_link in self.blogs_arr:
            blog_index = self.blogs_arr.index(blog_link)
            if 'img_pattern' in self.blogs[blog_index] and self.blogs[blog_index]['img_pattern']!='' :
                pattern = self.blogs[blog_index]['img_pattern']
            else:
                pattern = '.ct .box .pic a::attr(bigimgsrc)'
            #end if
        else:
            print(blog_link+' not found in blog_arr')
            self._add_log(blog_link+' not found in blog_arr')
            return
        #end if

        #pattern = '.imgwrapper'
        img_links = response.css(pattern).extract()
        print(str(len(img_links)) + ' pics to crawl//'+response.url)
        newOne = False
        for img in img_links:
            if self._save_pic(img, save_path, self._md5(img)+'.jpg'):
                newOne = True
            #end if
        #end
        
        #self.finished_album_names.append(str(user_id))
        if newOne:
            self._append_done_list(response.url)
            self.finished_album_num = self.finished_album_num + 1
            self._add_daily_log(save_path)
            self._log_done_album_name(save_path)
        #end if
    #end def


    def __save_path(self, blog):
        domain = blog.replace('http://', '')
        return os.path.join(self.save_path, domain)
    #end def


    def __parse_blog_index(self, url):
        matches = re.search(r'pos=(\d+)', url)
        if matches:
            return matches.group(1)
        else:
            return None
        # end if
    #end def

#end class

