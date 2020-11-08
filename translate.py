import logging
import time
from random import randint

from config import get_config

logger = logging.getLogger(__name__)

cfg = get_config("translator")


def get_translation(translator, description):
    try:
        translation = translator.translate(
            description, src="cs", dest=cfg["destination_language"]
        )
        time.sleep(randint(5, 10))
        description_pl = translation.text
        return description_pl
    except:
        logger.exception("Error during translation")
        return None
