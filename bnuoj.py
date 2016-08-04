# -*- coding:utf-8 -*-

import urllib
import urllib2
import cookielib
import re


# BNUOJ
class BNUOJ:
    def __init__(self):
        self.loginUrl = 'http://acm.bnu.edu.cn/v3/ajax/login.php'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
        self.headers = {'User-Agent': self.user_agent}
        self.spaceUrl = 'http://acm.bnu.edu.cn/v3/userinfo.php?name=caitouda'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'username': '******',
            'password': '******'
        })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def getPage(self):
        request = urllib2.Request(
            url=self.loginUrl,
            data=self.postdata,
            headers=self.headers)
        result = self.opener.open(request)
        result = self.opener.open(self.spaceUrl)
        # 打印登录内容
        print result.read().decode('utf-8')


bnuoj = BNUOJ()
bnuoj.getPage()
