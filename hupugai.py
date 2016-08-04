# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os


# 处理页面标签类
class Tool:
    # 去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>|<br.*?/>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # 将多行空行删除
    removeNoneLine = re.compile('\n+')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeNoneLine, "\n", x)
        # strip()将前后多余内容删除
        return x.strip()


class Spider:
    def __init__(self):
        self.siteURL = 'http://bbs.hupu.com/'
        self.tool = Tool()

    def getPage(self, pageIndex):
        url = self.siteURL + str(pageIndex) + '.html'
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        # print response.read().decode('gbk')
        return response.read().decode('gbk', 'ignore')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(
            '<div class="user">.*?<a href="(.*?)" target=.*?<img src="(.*?)" width=.*?<div class="floor_box">.*?target="_blank">(.*?)</a>',
            re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2]])
        return contents

    # 获取用户空间首页页面
    def getDetailPage(self, infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk', 'ignore')

    # 获取个人文字简介
    def getBrief(self, page):
        pattern = re.compile('<div class="personalinfo">(.*?)</div>', re.S)
        result = re.search(pattern, page)
        # print result.group(1)
        return self.tool.replace(result.group(1))

    # 获取页面所有图片
    def getAllImg(self, page):
        # pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
        # 个人信息页面所有代码
        # content = re.search(pattern,page)
        # 从代码中提取图片
        patternImg = re.compile('src="(.*?)"', re.S)
        images = re.findall(patternImg, page)
        return images

    # 保存多张写真图片
    def saveImgs(self, images, name):
        number = 1
        for imageURL in images:
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            # if len(fTail) > 3:
            # fTail = "jpg"
            if fTail == "jpg" or fTail == "png":
                fileName = name + "/" + str(number) + "." + fTail
                self.saveImg(imageURL, fileName)
                number += 1
        print u"发现", name, u"共有", number, u"张照片"

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    # 保存头像
    def saveIcon(self, iconURL, name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL, fileName)

    def saveBrief(self, content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, "w+")
        print u"正在偷偷保存她的个人信息为", fileName
        f.write(content.encode('utf-8'))

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return False

    # 将一页亮了的用户的信息保存起来
    def savePageInfo(self, pageIndex):
        # 获取第一页用户列表
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]空间首页URL,item[1]头像URL,item[2]姓名
            print u"发现一位用户,名字叫", item[2]
            print u"正在偷偷地保存", item[2], "的信息"
            print u"又意外地发现他的个人地址是", item[0]
            # 个人详情页面的URL
            detailURL = item[0]
            # 得到空间首页页面代码
            detailPage = self.getDetailPage(detailURL)
            # 获取个人简介
            brief = self.getBrief(detailPage)
            # 获取所有图片列表
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            # 保存个人简介
            self.saveBrief(brief, item[2])
            # 保存头像
            self.saveIcon(item[1], item[2])
            # 保存图片
            self.saveImgs(images, item[2])


spider = Spider()
spider.savePageInfo(15573215)
