from flask.ext.mail import Message

from app import app, mail

def send_email(to, subject, template):
    retcode = 1
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    try:
        mail.send(msg)
    except:
        retcode = 0

    return retcode
