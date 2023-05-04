
import psycopg2
import os
from pathlib import Path
from datetime import datetime
conn = psycopg2.connect(database="postgres",
                        host="202.28.34.202",
                        user="postgres",
                        password="cs@msu",
                        port="5432")
cursor = conn.cursor()


agency = {'SRO':1, 'TWV':2, 'SRG':3, 'K79':4, 'SME':5, 'VPC':6, 'VSU':7, 'XNE':8, 'SAI':9, 'BKB':10}
curr = 'VPC'

dirpath = 'D:\\project file\\Code project\\currency\\'+curr


paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
fn = paths[len(paths)-1]

with open(fn) as f:
    lines = f.readlines()


cursor.execute("SELECT * FROM exchanges where agencyid = "+ str(agency[curr]))
data = cursor.fetchall()
if(len(data) == 0) :
    for v in lines:
        if v != [] and v !='\n':
            d = v.split(' ')
            print(d[0])
            d[4] = d[4][0:len(d[4])-1]
            # cursor.execute("SELECT currencyid FROM currencies where cabb = '"+ str(d[0])+"'" )
            try:
                cursor.execute("SELECT currencyid FROM currencies where cabb = '" + str(d[0]) + "'")
                # cursor.execute("SELECT currencyid FROM currencies where cabb = 'USD'")
                id = cursor.fetchall()[0][0]
                ag =  agency[curr]
                # print("INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt) "
                #                "VALUES ("+str(id)+", "+str(ag)+", "+str(d[1])+", "+str(d[2])+", "+str(d[3])+","+str(d[4])+",1,'"+str(datetime.now())+"')")
                cursor.execute("INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) "
                               "VALUES ("+str(id)+", "+str(ag)+", "+str(d[1])+", "+str(d[2])+", "+str(d[3])+","+str(d[4])+",1,'"+str(datetime.now())+"',0,0)")
            except:
                print('cannot find currency')
                continue
            print('insert all the new currencies : completed')
    conn.commit()

else:

    for v in lines:
        if v != []:
            d = v.split(' ')
            d[4] = d[4][0:len(d[4]) - 1]
            try:
                cursor.execute("SELECT currencyid FROM currencies where cabb = '" + str(d[0])+"'")
                id = cursor.fetchall()[0][0]
                ag = agency[curr]

                cursor.execute("SELECT * from exchanges where "
                               "agencyid = "+str(ag)+" and "
                               "flag =1 and "
                               "currencyid = "+str(id)+" and "
                               "dem = "+str(d[3])+" and "
                               "dem2 = "+str(d[4])
                               )
                conn.commit()
                cdata = cursor.fetchall()
            except:
                print('cannot find the currency check'+d[0])
                continue

            if(len(cdata) == 0):

                cursor.execute("INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) VALUES (" + str(
                    id) + ", " + str(ag) + ", " + str(d[1]) + ", " + str(d[2]) + ", " + str(d[3]) + "," + str(d[4]) + ", 1,'"+str(datetime.now())+"',0,0)")
                conn.commit()
                print('add a new exchange '+ str(d))

            else:
                did = cdata[0][0]
                flag = False
                if(float(d[1])== cdata[0][3] and float(d[2])==cdata[0][4] and float(d[3])==float(cdata[0][5]) and float(d[4])==float(cdata[0][6])):
                    flag = False
                else:
                    cpbuy = float(d[1]) - float(cdata[0][3])
                    cpsel = float(d[2]) - float(cdata[0][4])
                    print("update: " + d[0])
                    cursor.execute("UPDATE exchanges set flag = 0 where id = " + str(did))
                    conn.commit()
                    cursor.execute("INSERT INTO exchanges (currencyid, agencyid, buy, sell, dem, dem2, flag, dt, cpbuy, cpsell) "
                                       "VALUES (" + str(id) + ", " + str(ag) + ", " + str(d[1]) + ", " + str(d[2]) + ", " + str(d[3]) + "," + str(d[4]) + ", 1,'"+
                                       str(datetime.now())+"', "+str(cpbuy)+","+str(cpsel)+")")
                    conn.commit()

print('update '+curr+' completed...at: '+str(datetime.now()))

cursor.close()

