import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

###########UPDATE##############
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# Fetch the service account key JSON file contents
cred = credentials.Certificate(
    './currencyexchangebc-firebase-adminsdk-jxsc0-94a937b494.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://currencyexchangebc-default-rtdb.firebaseio.com/'
})
##############UPDATE###############

url = "https://www.twelvevictory.com/exchange"
driver = webdriver.Edge(executable_path='C:/Users/shipd/Desktop/project file/Code project/msedgedriver.exe')
driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
all_divs = soup.find('div', {'class': 'container'}).text
# transcript = all_divs.find('table',class_ ='table')
li = soup.find_all('div', {'class': 'exch-rate-table'})
tr = soup.find_all('tbody',{'class':'tb-scroll'})
td = []
cur = []
dem = []
buy = []
sel = []
l = []

fina_list = []
tmp = []
p =1
for row in tr[0]:
    t = row.text.split('\n')   
    for x in t:
        if(len(x.strip())> 0):
            p += 1
            if(p == 1):
                x = fina_list.append('USD'[:3])
            if(p>5):
                fina_list.append(x.strip())
       
#print('PRINTBY TMP',tmp)
#for x in tmp[0]:
#    if (len(x.strip()) != 0) and (x.strip() !='Currency') and (x.strip() != 'Buy') and (x.strip() != 'Sell'):
#        fina_list.append(x.strip())

#print('PRINTBY Fina_list',fina_list)

flag = False
k =0
p=0
c=0
currency = ''
while(1):
    x = fina_list[k]
    if(x[0].isdigit() == False):
        currency = x
        cur.append(currency)
        if(len(fina_list[k+2].split('.')) < 2):
            dem.append(fina_list[k+2])
            buy.append(fina_list[k+3])
            sel.append(fina_list[k+4])
            k+=4
        else:
            dem.append('0-0')
            buy.append(fina_list[k + 2])
            sel.append(fina_list[k + 3])
            k+=3
    else:
        cur.append(currency)
        if (len(fina_list[k].split('.')) < 2):
            dem.append(fina_list[k + 0])
            buy.append(fina_list[k + 1])
            sel.append(fina_list[k + 2])
            k += 2
        else:
            dem.append('0-0')
            buy.append(fina_list[k + 0])
            sel.append(fina_list[k + 1])
            k += 1
    k+=1
    if k== len(fina_list):
        break

print(len(cur), len(sel), len(dem), len(buy))


rate = []
for i in range(len(dem)):
    d = {}
    c = cur[i]
    d['cur'] = c.strip()
    if(dem[i].find('-') > 0):
        if dem[i].split('-')[0].strip().isnumeric() and dem[i].split('-')[1].strip().isnumeric() and int( dem[i].split('-')[0].strip().replace(',','')) > int( dem[i].split('-')[1].strip().replace(',','')):
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


print(rate)

from datetime import datetime
fn = 'C:\\Users\\shipd\\Desktop\\project file\\Code project\\currency\\TWV\\'+str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))+'.txt'

###############UPDATE###############
#config apikey firebase mykey  https://projectend-266ec-default-rtdb.firebaseio.com/
firebase = firebase.FirebaseApplication(
    'https://currencyexchangebc-default-rtdb.firebaseio.com/', None
)
mydata = {
    'TWN'+str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S")): rate,
}
#save data to firebase real time
#ref = db.reference('WebExtract_TWV/')
#ref_extract = ref.child('TWV')
#ref_extract.update({
#    'TWV': rate,
#    'DatetimeUPDATE':str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
#})
###############UPDATE###############

#save to local file
with open(fn, 'w', encoding='utf-8') as data:
    for v in rate:
        data.write('%s %s %s %s %s\n' % (v['cur'], v['buy'], v['sell'], v['dem1'], v['dem2']))

driver.close()
print('done')

