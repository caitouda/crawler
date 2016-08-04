# -*- coding:utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import datetime
import time
import subprocess
import guji


class Myemail:
    # mailto_list = ["caitouda@163.com"]  # 目标邮箱
    getmailto_list = guji.GUJI()
    mailto_list = str(getmailto_list.getEmail())
    # mailto_list =
    mail_host = "smtp.163.com"
    mail_user = "******@163.com"
    mail_pass = "******"  # 163邮箱smtp生成的密码

    def send_mail(self, to_list, sub, content):
        me = "神秘用戶" + "<" + self.mail_user + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False


            # if __name__ == '__main__':
            # send_mail(mailto_list, '好消息來了', '必须要睡觉了哦')
            # test = Myemail()
            # test.send_mail(test.mailto_list, 'test', 'test')
