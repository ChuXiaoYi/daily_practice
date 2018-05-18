import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"      # SMTP服务器

sender = '895706056@qq.com'    # 发件人邮箱(最好写全, 不然会失败)
receivers = ['769438933@qq.com', 'a895706056@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

content = '滴滴～测试测试'
title = '我是阿联酋酋长'  # 邮件主题

def sendEmail():

    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login('895706056@qq.com', 'xgveecvwvnncbbeb')  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

if __name__ == '__main__':
    sendEmail()