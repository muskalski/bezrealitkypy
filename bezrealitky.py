import logging
import re
import sqlite3
import time
from datetime import datetime
from random import randint

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config import get_config
from email_sender import send_email
from translate import get_translation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler("bezrealitky.log"), logging.StreamHandler()],
)

cfg = get_config("bezrealitky")

translator = Translator()

conn = sqlite3.connect("flats.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS flats (id INTEGER PRIMARY KEY, is_new INTEGER, layout TEXT, size REAL, description TEXT,
price REAL, status TEXT, district TEXT, added TEXT, updated TEXT, description_pl TEXT)"""
)

base_url = "https://www.bezrealitky.cz"
price_from = cfg["price_from"]
price_to = cfg["price_to"]
districts = [x.strip() for x in cfg["districts"].split(",")]
layouts = ",".join([x.strip() for x in cfg["layouts"].split(",")])

retry_strategy = Retry(total=5, backoff_factor=5)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

while True:
    email_content = ""
    for district in districts:
        i = 1
        while True:
            url = f"{base_url}/vypis/nabidka-pronajem/byt/praha/praha-{district}/{layouts}?priceFrom={price_from}&priceTo={price_to}&equipped%5B0%5D=castecne&equipped%5B1%5D=vybaveny&page={i}"
            i += 1
            district = district.capitalize()
            logging.info(f"Scraping {district}...")
            try:
                r = requests.get(url, timeout=10)
            except:
                logging.exception("Get request from bezrealitky failed.")
            soup = BeautifulSoup(r.text, "html.parser")
            flats = soup.find_all("article", "product product--apartment has-ctas")
            if not flats:
                break
            for flat in flats:
                try:
                    flat_id = re.findall(r"\d+", flat["id"])[0]
                except IndexError:
                    continue
                prices = re.findall(
                    r"[0-9,]+",
                    flat.find("strong", "product__value").string.replace(".", ""),
                )
                total_price = sum(map(int, prices))
                description = flat.find("p", "product__info-text").string.strip()
                layout, size = re.findall(
                    r"[0-9+k]+", flat.find("p", "product__note").string
                )
                status = flat.find("span", "badge")
                datetime_now = datetime.now().isoformat()
                is_new = 0
                if status:
                    status = status.string
                    if "Nová nabídka" in status.string:
                        is_new = 1
                select_sql = "SELECT * FROM flats WHERE id=?"
                c.execute(select_sql, (flat_id,))
                selected_flat = c.fetchone()
                if selected_flat:
                    if selected_flat[4] != description:
                        description_pl = get_translation(translator, description)
                        update_description_sql = """UPDATE flats
                                 SET description = ?, description_pl = ?
                                 WHERE id = ?"""
                        c.execute(
                            update_description_sql,
                            (description, description_pl, flat_id),
                        )
                    update_sql = """UPDATE flats
                                 SET is_new = ?, layout = ?, size = ?, price = ?, status = ?, district = ?, updated = ?
                                 WHERE id = ?"""
                    update_parameters = (
                        is_new,
                        layout,
                        size,
                        total_price,
                        status,
                        district,
                        datetime_now,
                        flat_id,
                    )
                    c.execute(update_sql, update_parameters)

                else:
                    description_pl = get_translation(translator, description)
                    insert_parameters = (
                        flat_id,
                        is_new,
                        layout,
                        size,
                        description,
                        total_price,
                        status,
                        district,
                        datetime_now,
                        datetime_now,
                        description_pl,
                    )
                    insert_sql = "INSERT INTO flats (id, is_new, layout, size, description, price, status, district, added, updated, description_pl) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
                    link = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{flat_id}"
                    email_parameters = f"{link}\nDistrict: {district}\nIs new ad: {is_new}\nLayout: {layout}\nSize (m): {size}\nTotal price: {total_price}\nStatus: {status}\nCzech description: {description}\nTranslated description: {description_pl}\n\n\n"
                    logging.info(email_parameters)
                    email_content += email_parameters
                    c.execute(insert_sql, insert_parameters)
                conn.commit()

            time.sleep(randint(30, 60))
    if email_content:
        send_email(email_content)
