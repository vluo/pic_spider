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

from pic_spy.spiders.tuchong_album import TuchongSpider
from common import common_func


class DoubanSpider(TuchongSpider):
    name =  'douban_album'
    start_urls = []
    album_link = 'https://movie.douban.com/subject/{id}/photos?type=S&start={start_num}&sortby=like&size=a&subtype=a'
    pic_url = 'https://img3.doubanio.com/view/photo/raw/public/{pic_id}.jpg'
    allowed_domains = ["douban.com"]
    movies = []
    header = {}

    def __init__(self):
        super().__init__()
        self.movies = my_config.config.douban_movies
    #end def

    def start_requests(self):
        self.header = super()._getHeader()
        initRequests = []
        for movie in self.movies:
            print(movie)
            save_path = self.__save_path(movie['name'])
            album_link = self.album_link.format(id=movie['id'], start_num=0)  #self.api_url.replace('[num]', str(to_crawl_album_num))
            request = Request(album_link, callback=self.__parse_cover_list, method='GET', headers=self._getHeader())
            initRequests.append(request)
        #end for
        return initRequests
    #end def

    def __parse_cover_list(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> '+response.url)
            return None
        # end if

        covers = response.css('.cover a::attr(href)').extract()
        print(response.url+' '+str(len(covers))+' pages to  crawl')
        for cover in covers:
            yield Request(cover, callback=self.__parse_cover_page, method='GET', headers=self._getHeader())
        #end for

        nextPage = response.css('.paginator .next a::attr(href)').extract()
        if nextPage:
            print('next page >>> '+nextPage[0])
            yield Request(nextPage[0], callback=self.__parse_cover_list, method='GET', headers=self._getHeader())
        #end if
    #end def

    def __parse_cover_page(self, response):
        if response.status != 200 or response.text == '':
            self._add_log(response.url + ' request failed ' + str(response.status))
            print('request error >> '+str(response.status) + ' >>>>>>>>> ')
            return None
        # end if

        text = response.css('.magnifier a::attr(onclick)').extract()[0]
        pic_id = self.__parse_pic_id(text)
        if not pic_id:
            print('not pic id found')
            return None
        #end if
        ##print(pics)
        pic_url = self.pic_url.format(pic_id=pic_id)
        title = response.css('#title-anchor::text').extract()[0]
        title = title if title else 'douban_album'
        save_path = self.__save_path(title)
        self.header['Referer'] = response.url
        if self._save_pic(pic_url, save_path):
            # self.finished_pic_num = self.finished_pic_num +1
            newOne = True
        # end if

    #end def

    def _getHeader(self):
        return self.header
    #end def


    def __save_path(self, author):
        save_path = os.path.join(self.save_path, author)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        #end fi
        return save_path
    #end def

    def __parse_pic_id(self, text):
        matches = re.search(r'\'(\d+)\'', text)
        if matches:
            return matches.group(1)
        else:
            return None
        # end if
    #end def


#end class

