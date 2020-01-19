from flask import current_app, render_template
from flask_mail import Mail, Message

mail = Mail()


def send_mail(subject, recipient, body):

    msg = Message(subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[recipient])

    msg.body = body

    mail.send(msg)


def send_mail_from_template(subject, recipient, template, **template_kwargs):

    msg = Message(subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[recipient])

    msg.body = render_template('%s.txt' % template, **template_kwargs)
    msg.html = render_template('%s.html' % template, **template_kwargs)

    mail.send(msg)
