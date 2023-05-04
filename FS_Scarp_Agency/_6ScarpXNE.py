from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
try:
    firebase_admin.get_app()
except ValueError:
    app = firebase_admin.initialize_app(cred)
db = firestore.client()

company_name = 'XNE'
print("Scraping data "+company_name)
url = "https://www.x-one.co.th/#/"
driver = webdriver.Edge(
    executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
driver.get(url)
time.sleep(5)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
all_divs = soup.find('div', {'class': 'container'}).text
# transcript = all_divs.find('table',class_ ='table')
li = soup.find_all('div', {'class': 'table shadow'})
tr = soup.find_all('table', {'class': 'table'})
td = []
cur = []
dem = []
buy = []
sel = []
l = []
fina_list = []
rate = []
for row  in tr:
    x = row.text.split('\n')
    fina_list.append(x[6:len(x)])

for x in fina_list:
    p = 0
    for k in x:
        p += 1
        if k== '':
            p=0
        elif p==1:
            cur.append(k[0:3])
            dem.append(k[3:len(k)])
        elif p==2:
            buy.append(k)
        elif p==3:
            sel.append(k)



print(len(cur), len(sel), len(dem), len(buy))


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

    if(c =='JPY'):
        if float(buy[i]) > 10 or float(sel[i]) > 10  :
            d['buy']  = str(float(buy[i].strip())/100)
            d['sell'] = str(float(sel[i].strip())/100)
    elif (c == 'KRW'):
        if float(buy[i]) > 1 or float(sel[i]) > 1:
            d['buy'] = str(float(buy[i].strip()) / 100)
            d['sell'] = str(float(sel[i].strip()) / 100)
    else:
        d['buy'] = buy[i].strip()
        d['sell'] = sel[i].strip()

    rate.append(d)
        
print(d)

# Prepare the data to update
XNE = {
    u'agenName': company_name,
    u'agency': rate,
    u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
}

# Fetch the document with the matching agenName
docs = db.collection('testCurrency').where("agenName", "==", company_name).get()

# Check if a document was found
if len(docs) > 0:
    # Update the document with the new data
    for doc in docs:
        key = doc.id
        db.collection('testCurrency').document(key).update(XNE)
        print(f"Updated document {company_name} with key: {key}")
else:
    # If no document was found, create a new one
    db.collection('testCurrency').add(XNE)
    print("Created a new document "+company_name)

driver.close()
print('done')