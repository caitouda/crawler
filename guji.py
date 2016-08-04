# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import time
import sys


# 咕叽爬虫类
class GUJI:
    def getGuji(self):
        try:
            self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
            self.headers = {'User-Agent': self.user_agent}
            # self.url = 'http://www.weibo.com/u/2719507991'
            self.url = 'http://iguji.net/module/index.htm?defaultUser=true'
            request = urllib2.Request(self.url, headers=self.headers)
            response = urllib2.urlopen(request)
            # print response.read().decode('utf-8')
            # page = response.read()
            page = response.read().decode('utf-8', 'ignore')
            # print page
            return page
            # return response

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接咕叽失败,错误原因", e.reason
                return None

    def getFilm(self):
        page = self.getGuji()
        pattern = re.compile(
            'film=(.*?)email',
            re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  # 测试输出
            # print result
            result = result.group(1).strip()
            # print result
            return result.encode('utf-8')
        else:
            return None

    def getEmail(self):
        page = self.getGuji()
        pattern = re.compile(
            'email=(.*?)</div>',
            re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  # 测试输出
            # print result
            result = result.group(1).strip()
            # print result
            return result.encode('utf-8')
        else:
            return None
