#!/usr/bin/env python

import smtplib, jinja2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

smtp_url = 'smtp.gmail.com' #gmail server url
smtp_port = 587 #gmail server port
email_username = ''
email_password = ''
email_from = ''

def sendHTMLEmail(to, subject, body):
    server = smtplib.SMTP(smtp_url, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = to
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText(body, 'html')
    msgAlternative.attach(msgText)
    server.sendmail(email_from, to, msg.as_string())
    server.quit()

def renderJinjaTemplate(folder, f, context):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(folder)
        )
    return env.get_template(f).render(context)


def sendEmailTemplate(to, subject, context, template_file, template_folder=''):
    rendered_html = renderJinjaTemplate(template_folder, template_file,  context)
    sendHTMLEmail(to, subject, rendered_html)

context = {'name' : 'bob'}
sendEmailTemplate('', "Test Sub", context, 'user-receipt.html')
