import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

###########UPDATE##############

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Use a service account.
cred = credentials.Certificate('D:/project file/Code project/newKey260166.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
##############UPDATE###############
url = "https://valueplusexchange.com/#/"
driver = webdriver.Edge(executable_path='D:/project file/Code project/msedgedriver.exe')
driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
tr = soup.find_all('table')
td = []
cur = []
dem = []
buy = []
sel = []
l = []

final_list = []
tmp = []
p =0
flag = False

for row in tr[0]:
      t = row.text.split('\n')
      for x in t:
          if x != '':
              if x.strip() == 'USD':
                  flag = True
              if flag:
                  final_list.append(x.strip())


final_list.append('end')
final_list.append('end')
final_list.append('end')

k =0

currency = ''
while(1):
    x = final_list[k]
    if(x[0].isdigit() == False):
            currency = final_list[k][0:3]
            cur.append(currency)
            if k+3 == len(final_list):
                break
            if(final_list[k+3][0].isdigit()):
                if (len(final_list[k + 1]) > 1):
                    dem.append(final_list[k + 1].replace('(', '').replace(')', '').replace(',', ''))
                else:
                    dem.append('0-0')
                buy.append(final_list[k+2])
                sel.append(final_list[k+3])
                k+=3
            else:
                dem.append('0-0')
                buy.append(final_list[k + 1])
                sel.append(final_list[k + 2])
                k+=2

    k+=1
    if k== len(final_list):
        break

print(len(cur), len(sel), len(dem), len(buy))

rate = []
for i in range(len(dem)):
    d = {}
    c = cur[i]
    d['cur'] = c.strip()
    if(dem[i].find('-') > 0):
        if int( dem[i].split('-')[0].strip()) > int( dem[i].split('-')[1].strip()):
            d['dem1']  = dem[i].split('-')[1].strip()
            d['dem2']  = dem[i].split('-')[0].strip()
        else:
            d['dem1'] = dem[i].split('-')[0].strip()
            d['dem2'] = dem[i].split('-')[1].strip()
    else:
        if dem[i] == '':
            d['dem1'] = 0
            d['dem2'] = 0
        else:
            d['dem1']  = dem[i].strip()
            d['dem2']  = dem[i].strip()
    d['buy'] = buy[i].strip()
    d['sell'] = sel[i].strip()

    rate.append(d)

from datetime import datetime

# for k in rate:
#     print(k)
fn = 'D:\\project file\\Code project\\currency\\VPC\\' + \
    str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))+'.txt'
###############UPDATE###############
# Create an initial document to update
#add data to firestore
VPC = {
    u'agenName':'VPC',
    u'agency': rate,
    u'DateTimeUpdate':str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
}
#Extract_ref = db.collection(u'getCurrency').add(VPC)

# Udpdate:
docs = db.collection('getCurrency').where("agenName","==",'VPC').get()
for doc in docs:
        key = doc.id
        db.collection('getCurrency').document(key).update({"agency": rate,"DateTimeUpdate": str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))})

###############UPDATE###############
with open(fn,'w') as data:
    for v in rate:
        data.write('%s %s %s %s %s\n' % (v['cur'], v['buy'], v['sell'], v['dem1'], v['dem2']))
driver.close()
print('done')
#
