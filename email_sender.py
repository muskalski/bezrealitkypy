import logging
import time

from mailjet_rest import Client

logging = logging.getLogger(__name__)

api_key = '***REMOVED***'
api_secret = '***REMOVED***'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


def send_email(content):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "***REMOVED***",
                    "Name": "BEZREALITKYBOT"
                },
                "To": [
                    {
                        "Email": "***REMOVED***",
                        "Name": "Piotrek"
                    },
                    {
                        "Email": "***REMOVED***",
                        "Name": "Apolonia"
                    },

                ],
                "Subject": "[BEZREALITKYBOT] New apartments",
                "TextPart": content,
            }
        ]
    }

    # Send the message via our own SMTP server.
    for _ in range(5):
        try:
            result = mailjet.send.create(data=data)
            logging.info(result.status_code)
            return True
        except:
            logging.exception('Problem with sending an e-mail')
        time.sleep(10)
    return False
