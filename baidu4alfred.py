#  -*- coding:utf-8 -*-
import httplib
import json, re
import sys
import time
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')
pattern = re.compile('(.*?)(\[.*?\])(.*?)')
query = '{query}'.strip().replace('\\', '')

def invoke():
    now_time = time.time()
    conn = httplib.HTTPConnection("suggestion.baidu.com")
    conn.request("GET", "/su?wd=" + quote(query) +"&t=" + str(int(time.time())))  
    r1 = conn.getresponse() 
    suggest_text = r1.read().decode('gbk') #百度suggest回数为gbk编码
    conn.close()
    return join_xml(suggest_text)

def init():
    print invoke()

def join_xml(text):
    match = pattern.search(text)
    json_data = json.loads(match.group(2))

    result = ['<?xml version="1.0"?>', '<items>']
    json_data.insert(0, query)

    i = 0
    for item in json_data:
        word = quote(item.encode('utf-8'))
        url = 'http://www.baidu.com/s?wd=' + word
        result.append('<item uid="baidusearch' + str(i) + '" arg="' + url + '">');
        result.append('<title>' + item + '</title>')
        result.append('<subtitle>搜索“' + item + '”</subtitle>')
        result.append('<icon>icon.png</icon>')
        result.append('</item>')  
        i += 1

    result.append('</items>')
    xml = ''.join(result)    
    return xml

init()    