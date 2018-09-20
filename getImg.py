#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
 
'''@author = 'Mickyqing'  '''
'''@time   = '2018年9月20日09:20:12' '''
 
from urllib import request, parse
import re
import os

def getJpg(data):
    jpglist = re.findall(r'<img(.*?)>', data)
    return jpglist

def getResponse(url):
    url_request = request.Request(url)    
    url_response = request.urlopen(url)
 
    return url_response

def downImg(start):
    global searchName
    global codeSearchName
    global n
    global picNum

    http_response = getResponse("https://www.duitang.com/search/?kw=" + codeSearchName + "&type=feed&include_fields=top_comments,is_root,source_link,item,buyable,root_id,status,like_count,like_id,sender,album,reply_count,favorite_blog_id&_=1537349450707&start=" + str(start)) #拿到http请求后的上下文对象(HTTPResponse object)
    jpg = re.findall(r'<img(.*?)>', http_response.read().decode('utf-8'))


    for x in jpg:
        path = re.findall(r'http.+?.jpeg', x)
        name = re.findall(r'alt="(.*?)"', x)
        imgid = re.findall(r'data-rootid="(.*?)"', x)

        if len(path) != 0 and len(name) != 0 and len(imgid) != 0:
            sub_http_response = getResponse('https://www.duitang.com/blog/?id=' + imgid[0])
            sub_path = re.findall(r'id="mbpho-img".+?src="(https.+?.jpeg)', sub_http_response.read().decode('utf-8'))

            if len(sub_path):
                print(sub_path[0])
                n = n + 1
                request.urlretrieve(sub_path[0], '.\\' + searchName + '\\' + name[0] + '_' + str(n) + '.jpg')

                if picNum <= n:
                    return False
    return True

def downPage(picNum):
    pageNum = int(picNum * 2 / 24)
    for i in range(pageNum):
        if not downImg(24 * i):
            break


n = 0
searchName = input('请输入搜索词：')
picNum = int(input('请输入想下载的图片个数：'))
codeSearchName = parse.quote(searchName)

dirs = os.path.dirname(os.path.realpath(__file__)) + '\\' + searchName

if not os.path.exists(dirs):
    os.mkdir(dirs);

downPage(picNum);
