import logging
import time

from mailjet_rest import Client

import config

cfg = config.get_config("email")

logger = logging.getLogger(__name__)

mailjet = Client(auth=(cfg["api_key"], cfg["api_secret"]), version="v3.1")


def send_email(content):
    data = {
        "Messages": [
            {
                "From": {"Email": cfg["from_email"], "Name": cfg["from_name"]},
                "To": [{"Email": cfg["to_email1"], "Name": cfg["to_name1"]}],
                "Subject": f"[{cfg['from_name']}] New apartments",
                "TextPart": content,
            }
        ]
    }

    for _ in range(5):
        try:
            result = mailjet.send.create(data=data)
            logging.info(result.status_code)
            return True
        except:
            logger.exception("Problem with sending an e-mail")
        time.sleep(10)
    return False
