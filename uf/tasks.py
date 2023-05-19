import calendar
import locale
import logging
from datetime import datetime, timedelta
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from celery import Celery

from uf.models import ValuesUF

app = Celery('uf')
logger = logging.getLogger(__name__)


@app.task()
def update_last_day_value():
    '''Add value of last day'''
    date = datetime.now() - timedelta(days=1)
    year = date.year
    number_month = date.month
    day = date.day
    url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # We configure the local language in Spanish for the search of the month
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    month = calendar.month_name[number_month]
    str_month = f'mes_{month}'
    element = soup.find("div", {"id": str_month})
    if not element:
        return
    table = element.find("table")
    rows = table.find_all("th")

    for row in rows:
        if row.text == str(day):
            try:
                date_value = date.date()
                ValuesUF.objects.get(date=date_value)
            except ValueError:
                pass
            except ValuesUF.DoesNotExist:
                if row.find_next("td").text:
                    string_value = (row.find_next("td").text).replace(".","").replace(",",".")
                    ValuesUF.objects.create(date=date_value, value=Decimal(string_value))
                    logger.info('Se creo el valor de la unida de fomento para el dia {} de {} de {}'.format(
                        day,
                        month,
                        year
                    ))
