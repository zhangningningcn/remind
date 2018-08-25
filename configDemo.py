# -*- encoding:utf-8 -*-

"""
这是个demo使用时拷贝一份改名为 config.py 然后修改配置
"""

emailuser="123@xx.com"  #用于登陆的账号，一般和发邮件的邮箱地址相同
emailaddr="123@xx.com"  #用于发送邮件的邮箱地址
smtp_server="smtp.xx.com" #邮箱smtp服务器地址
smtpport=25 #邮箱smtp服务器端口
passwdmail="password"

emailToAddr = '"name" <user1@xx.com>'
emailCcAddr = '"name1" <user2@xx.com> , "name2" <user3@xx.com> '
emailFromAddr = '"name" <' + emailaddr + '>'
BankList = (("a",1),("b",2),("c",3)) #a,b,c是银行的名字; 1,2,3是对应日期

