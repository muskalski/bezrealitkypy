import re
import sqlite3
from datetime import datetime

import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('flats.db')
c = conn.cursor()


base_url = 'https://www.bezrealitky.cz/'

price_from = 7500
price_to = 17000
district = 'nusle'
url = f'https://www.bezrealitky.cz/vypis/nabidka-pronajem/byt/praha/praha-{district}/1-1,2-kk,2-1?priceFrom={price_from}&priceTo={price_to}&equipped%5B0%5D=castecne&equipped%5B1%5D=vybaveny'

print(url)
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
soup.find('p')
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
    sql = 'INSERT INTO flats (id, is_new, layout, size, description, price, status, district, added) VALUES (?,?,?,?,?,?,?,?,?)'
    parameters = (flat_id, is_new, layout, size, description, total_price, status, district.capitalize(), datetime_now,)
    print(sql)
    c.execute(sql, parameters)
    conn.commit()

c.close()
