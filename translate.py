import time
from random import randint


def translate(translator, description):
    try:
        translation = translator.translate(description, src='cs', dest='pl')
        time.sleep(randint(5, 10))
        description_pl = translation.text
        return description_pl
    except:
        return None

