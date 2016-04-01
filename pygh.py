# _*_ coding: utf-8 _*_
import re
import urllib
import urllib2
import os, sys
import random
import time


def openurl(url):
    headers = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
               'Referer': 'http://www.gamersky.com'
               }
    request = urllib2.Request(url, headers=headers)
    reponse = urllib2.urlopen(request)
    if reponse.getcode() != 200:
        print u"URL请求失败,URL:", url
        jquery = []
        return jquery
    else:
        jquery = reponse.read()
        return jquery


# create page urls
def getallurl():
    headers = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 \
             (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
               'Referer': 'http://www.gamersky.com/ent/wp/'
               }
    pageurl = 'http://db2.gamersky.com/LabelJsonpAjax.aspx?callback=jQuery&jsondata=%7B%22type%22%3A%22getlabelpage%22%2C%22' \
              '/currentPage%22%3A1%2C%22pagesize%22%3A%2214%22%2C%22recordCount%22%3A%22221%22%2C%22pagesDisplay%22%3A6%7D&'
    request = urllib2.Request(pageurl, headers=headers)
    reponse = urllib2.urlopen(request)
    jquery = reponse.read()
    match = r'(?<=\>)\d.(?=\</a\>)'
    totalpage = (int)(re.findall(match, jquery)[0])
    print u'动态页数：', totalpage
    i = 0
    allurl = []

    for i in range(1, totalpage + 1, 1):
        dbrequest = 'http://db2.gamersky.com/LabelJsonpAjax.aspx?callback=jQuery&jsondata=%7B%22type%22%3A%22updatenodelabel%22%2C%22/' \
                    'isCache%22%3Atrue%2C%22cacheTime%22%3A60%2C%22nodeId%22%3A%2220117%22%2C%22isNodeId%22%3A%22true%22%2C%22page%22%3A' + str(
            i) + '%7D&'
        allurl.append(dbrequest)
    return allurl


# search page img  url
def getpageurl(url):
    jquery = openurl(url)
    pageurl = []
    divmatch = re.compile(r'<div\s{1}class=\\"img\\"><a\s{1}href=\\"http://www.gamersky.com/ent/\d{6}/\d{6}.shtml')
    picmatch = re.compile(r'http://www.gamersky.com/ent/\d{6}/\d{6}.shtml')
    divurl = re.findall(divmatch, jquery)
    for u in divurl:
        pageurl.append(re.findall(picmatch, u)[0])
    if len(pageurl) == 0:
        print u'分页链接错误'
    return pageurl


# check url
def checkurl(url):
    urlchange = re.findall(r'http://www.+\.jpg', url)
    if len(urlchange) == 0:
        return url
    else:
        urlchange = re.findall(r'(?<=\?)http://.+\.jpg', urlchange[0])
        return urlchange[0]


# search img url
def getimgurl(url):
    jquery = openurl(url)
    imgurl = []
    imgurl = re.findall(r"(?<=\?)http://.+\.jpg(?=\"\>\<img)", jquery)
    i = 0
    for urli in imgurl:
        imgurl[i] = checkurl(urli)
        i += 1
    lihtml = re.findall(r"(?<=li>)<a\s{1}href=.+(?=/li)", jquery)
    if len(re.findall(r'http:', lihtml[0])) == 0:
        lihtml = re.findall(r'(?<=pe100_page_contentpage).+\n.+\n.+\n', jquery)
        lihtml = re.findall('http://www.gamersky.com/ent/\d{6}/\d{6}_\d*.shtml', lihtml[0])
        for l in lihtml:
            jquery = openurl(l)
            iurl = re.findall(r"(?<=\?)http://.+\.jpg(?=\"\>\<img)", jquery)
            for i in iurl:
                imgurl.append(checkurl(i))
    else:
        listr = ""
        for l in lihtml:
            listr += l
        print listr
        liurl = re.findall(r'http://www.gamersky.com/ent/\d{6}/\d{6}_\d*.shtml', listr)
        for l in liurl:
            jquery = openurl(l)
            iurl = re.findall(r"(?<=\?)http://.+\.jpg(?=\"\>\<img)", jquery)
            for i in iurl:
                imgurl.append(i)
    print imgurl
    if len(imgurl) == 0:
        print u'图片地址搜索失败'
    return imgurl


# download pic
def loading(url, path):
    for l in url:
        path_jpg = path
        imgname = re.findall(r'\b\w+(?=.jpg)', l)[0]
        imgname += '.jpg'
        path_jpg += "/"
        path_jpg += imgname
        jquery = openurl(l)
        f = open(path_jpg, 'wb')
        f.write(jquery)
        f.close()
        print path_jpg


if __name__ == "__main__":
    allurl = getallurl()
    for dburl in allurl:
        pageurl = getpageurl(dburl)
        for p in pageurl:
            dirname = re.findall(r'\b\w+(?=.shtml)', p)[0]
            path = sys.path[0] + '/' + dirname
            if os.path.exists(path):
                os.mkdir(path)
            else:
                tail = ((str)(random.random()))[2:-1]
                path = path + '_' + tail
                os.mkdir(path)
            imgurl = getimgurl(p)
            loading(imgurl, path)
        time.sleep(10)
