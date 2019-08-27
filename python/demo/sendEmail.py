#!/usr/bin/env python
# coding=utf-8
import smtplib, sys, time
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

reload(sys)
sys.setdefaultencoding('utf8')


def main():
    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "xxxx@163.com"  # 用户名
    mail_pass = "xxxpwdxxx"  # 密码
    receivers = ['xxxx@163.com', 'xxxx@qq.com']  # 接收邮箱

    localtime = time.localtime(time.time())
    sender = mail_user

    # 发送的主题
    subject = u'{0}-{1}-{2} 标题'.format(localtime.tm_year, str(localtime.tm_mon).zfill(2),
                                       str(localtime.tm_mday).zfill(2))
    html = '<p>这里是邮件内容</p>'

    # message = MIMEText(u'Python 邮件发送中...', 'plain', 'utf-8')
    message = MIMEText(html, 'html', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message['From'] = formataddr([u'股票助手', sender])
    message['To'] = ",".join(receivers)
    # message['To'] = receivers[0]
    # message['To'] = formataddr(['客户', receivers[0]])
    # message['To'] = Header(str(receivers)[1:-1], 'utf-8')
    # message['To'] = formataddr([Header(u'客户1', 'utf-8'), receivers[0], Header(u'客户2', 'utf-8'), receivers[1]])

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号  outlook端口587  网易是25

    # smtpObj.ehlo()
    smtpObj.starttls()  # outlook 是此加密方式  网易默认，不用设置也可以
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

    print u"邮件发送成功"
    smtpObj.quit()


if __name__ == "__main__":
    main()
