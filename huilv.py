# -*- coding:utf-8 -*-


import urllib
import urllib2
import re
import myemail
import time


# 汇率爬虫类
class HL:
    # 传入页码，获取该页帖子的代码
    def getPage(self):
        try:
            url = 'http://www.kuaiyilicai.com/uprate/twd.html'
            # print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            # print response.read().decode('utf-8')
            page = response.read().decode('utf-8')
            return page
            # return response
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接汇率失败,错误原因", e.reason
                return None

    def getHl(self):
        page = self.getPage()
        pattern = re.compile(
            '<form class="form-horizontal" role="form">.*?<span style="color:Red;">(.*?)</span>',
            re.S)
        result = re.search(pattern, page)
        if result:
            print result.group(1)  # 测试输出
            return result.group(1).strip()
        else:
            return None


hl = HL()
sendtime = '16:15'
# timepattern = re.compile(r'20:54')
# timepattern = re.compile(r'hello')
while True:
    # sendtime = re.match(timepattern, '2016 3 1 20:54:54')
    # sendtime = re.match(timepattern, 'hellowhat')
    # sendtime = re.match(pattern, str(time.ctime()))
    # print str(time.ctime())
    if sendtime in str(time.ctime()):
        # print sendtime.group()  # 测试输出
        # print '成功了'
        todayhl = 1 / float(hl.getHl())
        test = myemail.Myemail()
        test.send_mail(test.mailto_list, '今天的匯率', str(round(todayhl, 4)))
        time.sleep(86000)
    else:
        print 'nothing'
    time.sleep(30)
