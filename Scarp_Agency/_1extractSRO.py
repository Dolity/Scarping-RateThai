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
app = firebase_admin.initialize_app(cred)
db = firestore.client()

url = "https://www.superrich1965.com/currency.php"
driver = webdriver.Edge(
    executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
driver.get(url)
time.sleep(5)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
all_divs = soup.find('div', {'class': 'container'}).text
li = soup.find_all('div', {'class': 'table shadow'})
tr = soup.find_all('table', {'class': 'table'})
td = []
agenciesid = []
cur = []
dem = []
buy = []
sel = []

for row in tr:
    td = row.findAll('td')
    k = 0
    for t in td:
        if (k % 5 == 0):
            cur.append(t.text[0:3])
        k += 1
    k = 0
    p = 0
    for t in td:
        x = str(t).split('<br/>')
        x[0] = x[0].split('>')[1].strip()
        x[len(x)-1] = x[len(x)-1].split('<')[0].strip()
        if (len(x[0]) > 0):
            if (x[0].find('<') < 0):
                k += 1
                if k == 1+p:
                    dem.append(x)
                elif k == 2+p:
                    buy.append(x)
                elif k == 3+p:
                    sel.append(x)
                    p += 3
    break
rate = []

#print("Cur\n",cur)
#print("DEM\n",dem)
#print("Buy\n",buy)
#print("Sell\n",sel)
print(len(cur), len(sel), len(dem), len(buy))


for i in range(len(dem)):
    c = cur[i]
    for j in range(len(dem[i])):
        d = {}
        d['cur'] = c.strip()
        if c == 'VND' or c == 'IDR':
            d['dem1'] = dem[i][j][2:6]
            d['dem2'] = dem[i][j][2:6]
        else:
            if (dem[i][j].find('-') > 0):
                d['dem1'] = dem[i][j].split('-')[1].strip()
                d['dem2'] = dem[i][j].split('-')[0].strip()
            else:
                d['dem1'] = dem[i][j].strip()
                d['dem2'] = dem[i][j].strip()
        d['buy'] = buy[i][j].strip()
        d['sell'] = sel[i][j].strip()
        rate.append(d)
        
# fn = 'D:\\project file\\Code project\\currency\\SRO\\' + \
#     str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))+'.txt'

###############UPDATE###############
#config apikey firebase mykey  https://projectend-266ec-default-rtdb.firebaseio.com/
#firebase = firebase.FirebaseApplication(
#    'https://currencyexchangebc-default-rtdb.firebaseio.com/', None
#)
#save data to firebase real time

# Create an initial document to update

SPO = {
    u'agenName': 'SPO',
    u'agency': rate,
    u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
}

#Extract_ref = db.collection(u'getCurrency').add(SPO)

# Udpdate:

# Fetch the document with the matching agenName
docs = db.collection('testCurrency').where("agenName", "==", 'SPO').get()

# Check if a document was found
if len(docs) > 0:
    # Update the document with the new data
    for doc in docs:
        key = doc.id
        db.collection('testCurrency').document(key).update(SPO)
        print(f"Updated document with key: {key}")
else:
    # If no document was found, create a new one
    db.collection('testCurrency').add(SPO)
    print("Created a new document")

driver.close()
print('done')

#Extract_ref.update({
#    'SPO': rate,
#    'DateTimeUPDATE':str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
#})

#doc_ref = db.collection(u'users').document(u'alovelace')
#doc_ref.set({
#    u'first': u'Ada',
#    u'last': u'Lovelace',
#    u'born': 1815
#})
# Update age and favorite color
#frank_ref.update({
#    u'age': 13,
#    u'favorites.color': u'Red'
#})
#+str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
#ref = db.collections('WebExtract_SPO/')
#ref_extract = ref.child('SPO')
#ref_extract.update({
#    'SPO': rate,
#    'DateTimeUPDATE':str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
#})
###############UPDATE###############


