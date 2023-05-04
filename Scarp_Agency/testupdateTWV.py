import psycopg2
import os
from pathlib import Path
from datetime import datetime


class ExchangeUpdater:
    def __init__(self, db_config, currency_code):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()
        self.agencies = {'SRO': 1, 'TWV': 2, 'SRG': 3, 'K79': 4, 'SME': 5, 'VPC': 6, 'VSU': 7, 'XNE': 8, 'SAI': 9, 'BKB': 10}
        self.currency_code = currency_code
        self.directory_path = os.path.join('D:', os.sep, 'project file', 'Code project', 'currency', self.currency_code)

    def update_exchange(self):
        paths = sorted(Path(self.directory_path).iterdir(), key=os.path.getmtime)
        latest_file = paths[-1]

        with open(latest_file) as f:
            lines = f.readlines()

        self.cursor.execute("SELECT * FROM exchanges WHERE agencyid = %s", (self.agencies[self.currency_code],))
        data = self.cursor.fetchall()
        if not data:
            for line in lines:
                if line and line != '\n':
                    parts = line.split(' ')
                    try:
                        self.cursor.execute("SELECT currencyid FROM currencies WHERE cabb = %s", (parts[0],))
                        currency_id = self.cursor.fetchone()[0]
                        agency_id = self.agencies[self.currency_code]
                        self.cursor.execute(
                            "INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) "
                            "VALUES (%s, %s, %s, %s, %s, %s, 1, %s, 0, 0)",
                            (currency_id, agency_id, parts[1], parts[2], parts[3], parts[4][:-1], datetime.now())
                        )
                    except psycopg2.Error:
                        print(f"Cannot find currency {parts[0]}")
                        continue
                print("Inserted all the new currencies: completed")
            self.conn.commit()

        else:
            for line in lines:
                if line:
                    parts = line.split(' ')
                    try:
                        self.cursor.execute("SELECT currencyid FROM currencies WHERE cabb = %s", (parts[0],))
                        currency_id = self.cursor.fetchone()[0]
                        agency_id = self.agencies[self.currency_code]

                        self.cursor.execute(
                            "SELECT * FROM exchanges WHERE agencyid = %s AND flag = 1 AND currencyid = %s AND "
                            "dem = %s AND dem2 = %s",
                            (agency_id, currency_id, parts[3], parts[4][:-1])
                        )
                        self.conn.commit()
                        currency_data = self.cursor.fetchall()

                    except psycopg2.Error:
                        print(f"Cannot find currency {parts[0]}")
                        continue

                    if not currency_data:
                        self.cursor.execute(
                            "INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) "
                            "VALUES (%s, %s, %s, %s, %s, %s, 1, %s, 0, 0)",
                            (currency_id, agency_id, parts[1], parts[2], parts[3], parts[4][:-1], datetime.now())
                        )
                        self.conn.commit()
                        print(f"Added a new exchange {parts}")