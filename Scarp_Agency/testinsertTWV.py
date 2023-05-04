import psycopg2
from pathlib import Path
from datetime import datetime
import os

# Connect to the database
conn = psycopg2.connect(database="postgres",
                        host="202.28.34.202",
                        user="postgres",
                        password="cs@msu",
                        port="5432")
cursor = conn.cursor()

# Dictionary of agency codes
agency = {'SRO': 1, 'TWV': 2, 'SRG': 3, 'K79': 4, 'SME': 5, 'VPC': 6, 'VSU': 7, 'XNE': 8, 'SAI': 9, 'BKB': 10}

# Currency to process
curr = 'TWV'

# Directory path for the currency files
dirpath = 'D:\\project file\\Code project\\currency\\' + curr

# Get the most recent file in the directory
paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
fn = paths[len(paths) - 1]

# Read the contents of the file
with open(fn) as f:
    lines = f.readlines()

# Fetch data from the database
cursor.execute("SELECT * FROM exchanges WHERE agencyid = %s", (agency[curr],))
data = cursor.fetchall()

# If there is no data for the given agency, insert all the new currencies
if len(data) == 0:
    for v in lines:
        if v != [] and v != '\n':
            d = v.split(' ')
            print(d[0])
            d[4] = d[4][0:len(d[4]) - 1]

            # Fetch the currency ID from the database
            cursor.execute("SELECT currencyid FROM currencies WHERE cabb = %s", (d[0],))
            id_data = cursor.fetchone()

            if id_data is None:
                print(f"Cannot find currency {d[0]} in the database")
                continue

            id = id_data[0]
            ag = agency[curr]

            # Insert the exchange data into the database
            cursor.execute("INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) "
                           "VALUES (%s, %s, %s, %s, %s, %s, 1, %s, 0, 0)",
                           (id, ag, d[1], d[2], d[3], d[4], datetime.now()))
            print(f"Inserted exchange data for {d[0]}")
    conn.commit()

# If there is data for the given agency, update the existing currencies
else:
    for v in lines:
        if v != []:
            d = v.split(' ')
            d[4] = d[4][0:len(d[4]) - 1]

            # Fetch the currency ID from the database
            cursor.execute("SELECT currencyid FROM currencies WHERE cabb = %s", (d[0],))
            id_data = cursor.fetchone()

            if id_data is None:
                print(f"Cannot find currency {d[0]} in the database")
                continue

            id = id_data[0]
            ag = agency[curr]

            cursor.execute("SELECT * FROM exchanges WHERE "
                           "agencyid = %s AND "
                           "flag = 1 AND "
                           "currencyid = %s AND "
                           "dem = %s AND "
                           "dem2 = %s",
                           (ag, id, d[3], d[4]))
