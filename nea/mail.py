import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate
from email.MIMEText import MIMEText


def send_mail(content):
    email_from = os.environ['DIGEST_MAIL']
    email_to = [os.environ['DIGEST_MAIL']]

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = COMMASPACE.join(email_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Weekly digest'

    msg.attach(MIMEText(content.encode('utf-8'), 'html'))

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.close()
