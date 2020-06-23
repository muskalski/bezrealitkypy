import logging
import smtplib
import time
from email.message import EmailMessage

logging = logging.getLogger(__name__)


def send_email(content, recipients=None):
    if recipients is None:
        recipients = ['***REMOVED***, ***REMOVED***']
    msg = EmailMessage()

    msg['Subject'] = f'[BEZREALITKYBOT] New apartments'
    msg['From'] = '***REMOVED***'
    msg['To'] = ", ".join(recipients)
    msg.set_content(content)
    p = '***REMOVED***'

    # Send the message via our own SMTP server.
    for _ in range(5):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.login('***REMOVED***', p)
            s.send_message(msg)
            s.quit()
            return True
        except:
            logging.exception('Problem with sending an e-mail')
        time.sleep(10)
    return False
