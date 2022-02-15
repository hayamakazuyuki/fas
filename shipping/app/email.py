from flask_mail import Message
from threading import Thread
from .extentions import mail

def send_email(subject, recipients, body, filename, attachment):
    msg = Message(subject, recipients=recipients, body=body)
    msg.attach(filename, 'text/csv', attachment)
    mail.send(msg)
