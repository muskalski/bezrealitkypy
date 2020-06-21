import logging
import re
import sqlite3
import time
from datetime import datetime
from random import randint
from googletrans import Translator

import requests
from bs4 import BeautifulSoup

from email_sender import send_email
from translate import translate

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler('bezrealitky.log'),
        logging.StreamHandler()
    ]
)

translator = Translator()

conn = sqlite3.connect('flats.db')
c = conn.cursor()

base_url = 'https://www.bezrealitky.cz/'

price_from = 7500
price_to = 17000
districts = ['karlin', 'zizkov', 'nove-mesto', 'stare-mesto', 'josefov', 'vinohrady', 'liben']


while True:
    email_content = ''
    for district in districts:
        url = f'https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt/praha/praha-{district}/1-1,2-kk,2-1?priceFrom={price_from}&priceTo={price_to}&equipped%5B0%5D=castecne&equipped%5B1%5D=vybaveny'
        logging.info(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        flats = soup.find_all('article', 'product product--apartment has-ctas')
        for flat in flats:
            try:
                flat_id = re.findall(r'\d+', flat['id'])[0]
            except IndexError:
                continue
            prices = re.findall(r'[0-9,]+', flat.find('strong', 'product__value').string.replace('.', ''))
            total_price = sum(map(int, prices))
            description = flat.find('p', 'product__info-text').string.strip()
            layout, size = re.findall(r'[0-9+k]+', flat.find('p', 'product__note').string)
            status = flat.find('span', 'badge')
            datetime_now = datetime.now().isoformat()
            is_new = 0
            if status:
                status = status.string
                if 'Nová nabídka' in status.string:
                    is_new = 1
            select_sql = 'SELECT * FROM flats WHERE id=?'
            c.execute(select_sql, (flat_id,))
            selected_flat = c.fetchone()
            if selected_flat:
                if selected_flat[4] != description:
                    description_pl = translate(translator, description)
                    update_description_sql = '''UPDATE flats
                             SET description = ?, description_pl = ?
                             WHERE id = ?'''
                    c.execute(update_description_sql, (description, description_pl, flat_id))
                update_sql = '''UPDATE flats
                             SET is_new = ?, layout = ?, size = ?, price = ?, status = ?, district = ?, updated = ?
                             WHERE id = ?'''
                update_parameters = (is_new, layout, size, total_price, status, district.capitalize(), datetime_now, flat_id)
                c.execute(update_sql, update_parameters)

            else:
                description_pl = translate(translator, description)
                insert_parameters = (flat_id, is_new, layout, size, description, total_price, status, district.capitalize(), datetime_now, 1, description_pl)
                insert_sql = 'INSERT INTO flats (id, is_new, layout, size, description, price, status, district, added, notification_sent, description_pl) VALUES (?,?,?,?,?,?,?,?,?,?,?)'
                link = f'https://www.bezrealitky.cz/nemovitosti-byty-domy/{flat_id}'
                email_parameters = (is_new, layout, size, description_pl, total_price, status, district)
                email_content += f'{link}\n{email_parameters}\n\n\n'
                logging.info(msg=(link, email_parameters))
                c.execute(insert_sql, insert_parameters)

        time.sleep(randint(30, 60))
    conn.commit()
    if email_content:
        send_email(email_content)
c.close()
