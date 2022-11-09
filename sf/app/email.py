from flask_mail import Message
from .extentions import mail

def send_email(subject):
    msg = Message(subject)
    msg.recipients = ['hayamak@i.softbank.jp']
    msg.body = 'メールの送信'
    mail.send(msg)
