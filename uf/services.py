import calendar
import locale
import logging
from datetime import datetime
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from celery import Celery

from uf.models import ValuesUF

app = Celery('uf')
logger = logging.getLogger(__name__)


class CreateValues():

    def create_all_value(self):
        for year in range(2013, datetime.now().year+1):
            self.create_data(str(year))

    def create_data(year):
        '''Create data from year'''
        url = f"https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        # We configure the local language in Spanish for the search of the month
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        all_month = list(calendar.month_name[1:])
        for index, month in enumerate(all_month):
            str_month = f'mes_{month}'
            element = soup.find("div", {"id": str_month})

            if not element:
                continue
            table = element.find("table")
            rows = table.find_all("tr")
            for row in rows:
                columns = row.find_all("th")
                if columns[0].text == month.capitalize():
                    continue

                for column in columns:
                    number_month = index + 1
                    if not column.text:
                        continue
                    day = column.text
                    try:
                        date_value = datetime(int(year), int(number_month), int(day)).date()
                        ValuesUF.objects.get(date=date_value)
                    except ValueError:
                        pass
                    except ValuesUF.DoesNotExist:
                        if column.find_next("td").text:
                            string_number = (column.find_next("td").text).replace(".","").replace(",",".")
                            ValuesUF.objects.create(date=date_value, value=Decimal(string_number))
