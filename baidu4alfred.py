#  -*- coding:utf-8 -*-
import httplib
import json, re
import sys
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')
pattern = re.compile('(.*?)(\[.*?\])(.*?)')

def invoke():
    conn = httplib.HTTPConnection("suggestion.baidu.com")
    conn.request("GET", "/su?wd=" + quote('{query}') +"&p=3&cb=window.bdsug.sug&sid=1427_1945_1788&t=1363856968686")  
    r1 = conn.getresponse() 
    suggest_text = r1.read().decode('gbk') #百度suggest回数为gbk编码
    conn.close()
    return parse_suggestdata(suggest_text)

def init():
    print invoke()

def parse_suggestdata(text):
    match = pattern.search(text)
    json_data = json.loads(match.group(2))

    result = ['<?xml version="1.0"?>', '<items>']

    for item in json_data:
        word = quote(item.encode('utf-8'))
        url = 'http://www.baidu.com/s?wd=' + word
        result.append('<item uid="baidusearch" arg="' + url + '">');
        result.append('<title>' + item + '</title>')
        result.append('<subtitle>baidu search</subtitle>')
        result.append('<icon>icon.png</icon>')
        result.append('</item>')  
    result.append('</items>')
    xml = ''.join(result)    
    return xml

init()    