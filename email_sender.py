import smtplib

from email.message import EmailMessage


def send_email(content):
    msg = EmailMessage()

    msg['Subject'] = f'[BEZREALITKYBOT] New apartments'
    msg['From'] = '***REMOVED***'
    msg['To'] = '***REMOVED***, ***REMOVED***'
    msg.set_content(content)

    # Send the message via our own SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login('***REMOVED***', '***REMOVED***')
    s.send_message(msg)
    s.quit()
