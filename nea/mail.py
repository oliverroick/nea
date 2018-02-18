import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate
from email.MIMEText import MIMEText


def send_mail(content):
    email_from = os.environ['DIGTEST_MAIL']
    email_to = [os.environ['DIGTEST_MAIL']]

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = COMMASPACE.join(email_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Weekly digest'

    msg.attach(MIMEText(content, 'html'))

    smtp = smtplib.SMTP('localhost', 1025)
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.close()
