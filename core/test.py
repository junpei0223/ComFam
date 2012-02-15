# -*- coding: utf-8 -*-
import urllib2
import base64

username = 'junpei'
password = 'qp56jk'
url = 'http://localhost:8080/rest/Tweet'

base64string =  base64.encodestring('%s:%s' % (username, password))[:-1]
authheader = 'Basic %s' % base64string

req = urllib2.Request(url)
req.add_header("Authorization", authheader)
handle = urllib2.urlopen(req)
print handle.read()
