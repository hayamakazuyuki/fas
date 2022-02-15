from flask_mail import Message
from threading import Thread
from .extentions import mail
# from flask import current_app

# not working
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_email(subject, recipients, body, filename, attachment):
#     msg = Message(subject, recipients=recipients, body=body)
#     msg.attach(filename, 'text/csv', attachment)
#     app = current_app
#     Thread(target=send_async_email, args=(app, msg)).start()


# this is working
def send_email(subject, recipients, body, filename, attachment):
    msg = Message(subject, recipients=recipients, body=body)
    msg.attach(filename, 'text/csv', attachment)
    mail.send(msg)
