# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import myemail
import time
import sys
import guji


# 电影天堂爬虫类
class DYTT:
    # 传入页码，获取该页帖子的代码
    def getPage(self, keyword):
        try:
            url = 'http://s.kujian.com/plus/search.php?kwtype=0&searchtype=title&keyword='
            # print url
            url = url + keyword
            # print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read().decode('utf-8')
            # page = response.read()
            page = response.read().decode('gbk', 'ignore')
            # print page
            return page
            # return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接电影天堂失败,错误原因", e.reason
                return None

    def getDytt(self):
        page = self.getPage(film)
        pattern = re.compile(
            '<div class="co_content8">.*?<b><a href=(.*?)>',
            re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  # 测试输出
            # print result
            result = result.group(1).strip()
            result = re.sub(re.compile("'"), "", result)
            print result
            return result
        else:
            return None

    def getNewurl(self):
        newurl = 'http://www.ygdy8.com'
        newurl = newurl + str(self.getDytt())
        # newurl = newurl + ftp.replace("'", '')
        # print newurl
        response = urllib2.urlopen(newurl)
        return response.read().decode('gbk', 'ignore')

    def getFtp(self):
        page = self.getNewurl()
        pattern = re.compile(
            '<a href="ftp:.*?>(.*?)</a>',
            re.S)
        result = re.search(pattern, page)
        if result:
            # print result.group(1)  # 测试输出
            # print result
            result = result.group(1).strip()
            print result
            # result = re.sub(re.compile("'"), "", result)
            return result.encode('utf-8')
        else:
            return None


firstfilm = '%B9%A4%B3%A7%B5%C4%B4%F3%C3%C5'
while True:
    dytt = DYTT()
    iguji = guji.GUJI()
    film = str(iguji.getFilm())
    biaoti = '电影《' + film + '》的下载链接'
    # print film
    # print keyword
    # print urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
    # ckeyword.decode('gbk')
    # print keyword
    # print urllib.quote(keyword.decode(sys.stdin.encoding).encode('gbk'))
    film = urllib.quote(film.decode(sys.stdin.encoding).encode('gbk'))
    # print film
    if film in firstfilm:
        print '您已经查询过这部电影'
    else:
        firstfilm = film
        test = myemail.Myemail()
        test.send_mail(test.mailto_list, biaoti, str(dytt.getFtp()))
    time.sleep(30)
