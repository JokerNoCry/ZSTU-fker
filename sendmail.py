#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Mail:
    def __init__(self, sender, receivers):
        # 第三方 SMTP 服务

        self.mail_host="smtp.qq.com"       #设置服务器:这个是qq邮箱服务器
        self.mail_pass="*********"           #授权码  需到服务提供商处获取
        self.sender = sender      #你的邮箱地址 
        self.receivers = receivers  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    def send(self, subject, content, sender_name, receivers_name):

        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header(sender_name, 'utf-8')   
        message['To'] =  Header(receivers_name[0], 'utf-8')     # 收件人名字，但只能传字符串，因此取列表第一个
        message['Subject'] = Header(subject, 'utf-8') 
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465) 
            smtpObj.login(self.sender,self.mail_pass)  
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')



if  __name__ == '__main__':
    sender = '********'    # 发件人邮箱
    receivers = ['********']    # 收件人列表
    subject = 'test subject'  # 发送的主题
    content = 'This is test content'  # 发送的内容
    sender_name = "*****"       # 发件人姓名
    receivers_name = ['********']   # 收件人姓名

    mail = Mail(sender, receivers)
    mail.send(subject, content, sender_name, receivers_name)