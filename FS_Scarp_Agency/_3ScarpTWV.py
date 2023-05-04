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

company_name = 'TWV'
url = "https://www.twelvevictory.com/exchange"
driver = webdriver.Edge(
    executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
driver.get(url)
time.sleep(5)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
all_divs = soup.find('div', {'class': 'container'}).text
li = soup.find_all('div', {'class': 'exch-rate-table'})
tr = soup.find_all('table',{'class':'text-nowrap nowrap-controller w-100'})
td = []
cur = []
dem = []
buy = []
sel = []
l = []
flag = False
p =0
fina_list = []

for row in tr[0]:
    t = row.text.split('\n')   
    for x in t:
        if(len(x.strip())> 0):
            p += 1
            if(p == 1):
                x = fina_list.append('USD'[:3])
            if(p>5):
                fina_list.append(x.strip())

p=1
c=0
currency = ""
k = 0
flag = True
for x in fina_list:
    if len(x.split('-')[0]) > 0:
        if x.split('-')[0][0].isdigit() == False:
            if(p == 1):
                fina_list.append('USD')
            p+=1
            if(p%2==0):
                currency = x
                print(currency)
                c=0
                k=0
                flag = True
        elif flag:
            c+=1
            if c==k+1:
                cur.append(currency)
                dem.append(x)
            if c==k+2:
                buy.append(x)
            if c==k+3:
                sel.append(x)
                k += 3
    else:
         flag = False

print(len(cur), len(sel), len(dem), len(buy))


rate = []
for i in range(len(dem)):
    d = {}
    c = cur[i]
    d['cur'] = c.strip()
    if(dem[i].find('-') > 0):
        if ( dem[i].split('-')[0].strip()) > ( dem[i].split('-')[1].strip()):
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

    # Add print statements to debug the issue
    print(f'sel length: {len(sel)}, i: {i}')
    if i < len(sel):
        d['sell'] = sel[i].strip()
        print(f'sel value: {sel[i]}')
    else:
        d['sell'] = ''
    rate.append(d)

print(rate)

# Prepare the data to update
TWV = {
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
        db.collection('testCurrency').document(key).update(TWV)
        print(f"Updated document with key: {key}")
else:
    # If no document was found, create a new one
    db.collection('testCurrency').add(TWV)
    print("Created a new document")

driver.close()
print('done')