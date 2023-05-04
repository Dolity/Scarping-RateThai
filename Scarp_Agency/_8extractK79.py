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
cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
##############UPDATE###############

url = "https://www.k79exchange.com/"
driver = webdriver.Edge(executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
# all_divs = soup.find('div', {'class': 'container'}).text
# transcript = all_divs.find('table',class_ ='table')
# li = soup.find_all('div', {'class': 'table shadow'})
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

t = tr[3].text.split('\n')

for x in t:
   if len(x) > 0:
       tmp.append(x)


final_list = tmp[5:len(tmp)]

# for x in final_list:
#     print(x)

k=0

while(1):
    x = final_list[k]
    if(x[0].isdigit() == False):
            t = final_list[k].split(' ')
            if len(t) > 1:
                cur.append(t[0].strip())
                dem.append(t[1].strip().replace(',',''))
                buy.append(final_list[k+1])
                sel.append(final_list[k+2])
                k+=2
            else:
                cur.append(t[0].strip())
                dem.append('0-0')
                buy.append(final_list[k + 1])
                sel.append(final_list[k + 2])
                k += 2
    k+=1
    if k== len(final_list):
        break

print(len(cur), len(sel), len(dem), len(buy))
#
# #
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
###############UPDATE###############
###############UPDATE###############
# Create an initial document to update
#add data to firestore
K79 = {
    u'agenName':'K79',
    u'agency': rate,
    u'DateTimeUpdate':str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
}
#Extract_ref = db.collection(u'getCurrency').add(K79)

# Udpdate:
docs = db.collection('testCurrency').where("agenName","==",'K79').get()
for doc in docs:
        key = doc.id
        db.collection('testCurrency').document(key).update({"agency": rate,"DateTimeUpdate": str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))})

###############UPDATE###############
###############UPDATE###############

driver.close()
print('done')
#
