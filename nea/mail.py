import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(content):
    email_from = os.environ['DIGEST_MAIL']
    email_to = [os.environ['DIGEST_MAIL']]

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = ', '.join(email_to)
    msg['Subject'] = 'Weekly digest'

    body = MIMEText(content, 'html')
    msg.attach(body)

    smtp = smtplib.SMTP('localhost', 1025)
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.close()
