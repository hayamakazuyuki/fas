from flask_mail import Message
from app import mail

# from flask import current_app
# from threading import Thread


# not working
# def send_async_email(msg):
#     with current_app.app_contex():
#         mail.send(msg)

# def send_email(subject, recipients, body, filename, attachment):
#     msg = Message(subject, recipients=recipients, body=body)
#     msg.attach(filename, 'text/csv', attachment)
#     Thread(target=send_async_email, args=msg).start()


# this is working
def send_email(subject, recipients, body, filename, attachment):
    msg = Message(subject, recipients=recipients, body=body)
    msg.attach(filename, 'text/csv', attachment)
    mail.send(msg)
