from flask_mail import Message
from .extentions import mail


def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients, body=body)
    # msg.attach(filename, 'text/csv', attachment)
    # Thread(target=send_async_email, args=(msg,)).start()

    mail.send(msg)

# def send_email(subject, recipients, body, filename, attachment):
#     msg = Message(subject, recipients=recipients, body=body)
#     msg.attach(filename, 'text/csv', attachment)
#     Thread(target=send_async_email, args=(msg,)).start()
    