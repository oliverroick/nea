import os
import smtplib
from email.message import EmailMessage


def send_mail(content):
    email_from = os.environ['DIGEST_MAIL']
    email_to = [os.environ['DIGEST_MAIL']]

    msg = EmailMessage()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Subject'] = 'Weekly digest'

    msg.set_content(content)

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.close()
