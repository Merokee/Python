# !/usr/bin/env python
# _*_ coding:utf-8 _*_
# author: zero
# datetime:18-7-11 下午3:25
import urllib
import urllib2

username = 'ubuntu'
password = 'zero123456'
webServer = 'http://45.40.194.111'

# 构建账号密码管理器
passwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
passwdmgr.add_password(None, webServer, username, password)

# 创建认证处理器
httpauth_handler = urllib2.HTTPBasicAuthHandler(passwdmgr)

# 创建opener对象
opener = urllib2.build_opener(httpauth_handler)

# 定义opener为全局opener，即保持登陆状态
urllib2.install_opener(opener)

# 构建request对象
request = urllib2.Request(webServer)

response = urllib2.urlopen(request)

print(response.read())