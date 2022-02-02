from flask_mail import Message
# from threading import Thread
from .extentions import mail


# def send_async_email(msg):
#     app = current_app()
#     with app.app_context():
#         mail.send(msg)


def send_email(subject, recipients, body, filename, attachment):
    msg = Message(subject, recipients=recipients, body=body)
    msg.attach(filename, 'text/csv', attachment)
    # Thread(target=send_async_email, args=(msg,)).start()

    mail.send(msg)

# def send_email(subject, recipients, body, filename, attachment):
#     msg = Message(subject, recipients=recipients, body=body)
#     msg.attach(filename, 'text/csv', attachment)
#     Thread(target=send_async_email, args=(msg,)).start()
    