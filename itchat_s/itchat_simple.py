# -*- coding: utf-8 -*-
# --------------------------------------
#       @Time    : 2018/8/16 下午6:08
#       @Author  : cxy =.= 
#       @File    : itchat_simple.py
#       @Software: PyCharm
# --------------------------------------
import itchat


@itchat.msg_register([itchat.content.TEXT, itchat.content.PICTURE], isGroupChat=True)
def text_reply(msg):
    if type(msg.text) != 'str':
        msg.download(msg.fileName)
    print("收到：{}".format(msg.text))


itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.send('hello', toUserName='@8f03e24dcb83755e6709db3485f86d1b48cd9142515efc2f3b77c992466f5897')
friend_list = itchat.get_friends(update=True)
for friend in friend_list:
    print(friend)

itchat.run()
