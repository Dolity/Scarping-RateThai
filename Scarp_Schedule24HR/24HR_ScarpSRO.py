import schedule
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def Rate_Thai():
    
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    
        # โค้ดการ scrape data ที่ต้องการ
    # Use a service account.
    company_name = 'SRO'
    print("Scraping data "+company_name)

    # เพิ่มโค้ด Web Scraping จากไฟล์อื่นๆ ตามต้องการ
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
    print(d)

    # Prepare the data to update
    SRO = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(SRO)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(SRO)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def Rate_SRO():
    
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    
        # โค้ดการ scrape data ที่ต้องการ
    # Use a service account.
    company_name = 'SRO'
    print("Scraping data "+company_name)

    # เพิ่มโค้ด Web Scraping จากไฟล์อื่นๆ ตามต้องการ
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
    print(len(cur), len(sel), len(dem), len(buy))
    rate.append({'agen': company_name})
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
    print(rate)

    # Prepare the data to update
    SRO = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(SRO)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(SRO)
        print("Created a new document "+company_name)

    driver.close()
    print('done')
    
def Rate_SRG():
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    
    company_name = 'SRG'
    print("Scraping data "+company_name)
    url = "https://www.superrichthailand.com/#!/en/exchange"

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

    row = tr[0].text
    k = row.split('\n')
    p = 0
    fina_list = []
    for x in k:
        if (len(x.strip()) > 0):
            p += 1
            if (p > 5):
                fina_list.append(x.strip())

    p = 1
    c = 0
    currency = ""
    k = 0
    flag = True
    for x in fina_list:
        if len(x.split('-')[0]) > 0:
            if x.split('-')[0][0].isdigit() == False:
                p += 1
                if (p % 2 == 0):
                    currency = x
                    c = 0
                    k = 0
                    flag = True
            elif flag:
                c += 1
                if c == k+1:
                    cur.append(currency)
                    dem.append(x)
                if c == k+2:
                    buy.append(x)
                if c == k+3:
                    sel.append(x)
                    k += 3
        else:
            flag = False


    print(len(cur), len(sel), len(dem), len(buy))

    rate = []
    rate.append({'agen': company_name})
    for i in range(len(dem)):
        d = {}
        c = cur[i]
        d['cur'] = c.strip()
        if (dem[i].find('-') > 0):
            if float(dem[i].split('-')[0].strip()) > float(dem[i].split('-')[1].strip()):
                d['dem1'] = dem[i].split('-')[1].strip()
                d['dem2'] = dem[i].split('-')[0].strip()
            else:
                d['dem1'] = dem[i].split('-')[0].strip()
                d['dem2'] = dem[i].split('-')[1].strip()
        else:
            if dem[i] == '':
                d['dem1'] = 0
                d['dem2'] = 0
            else:
                d['dem1'] = dem[i].strip()
                d['dem2'] = dem[i].strip()
        d['buy'] = buy[i].strip()
        d['sell'] = sel[i].strip()

        rate.append(d)
    print(d)
    # Prepare the data to update
    SRG = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(SRG)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(SRG)
        print("Created a new document "+company_name)

    driver.close()
    print('done')


#BAN TWV cause Scarping not work!? Un handle
def Rate_TWV():
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    company_name = 'TWV'
    print("Scraping data "+company_name)
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
    
    rates = []
    for i in range(len(cur)):
        rate = {}
        rate['cur'] = cur[i]
        rate['dem1'] = dem[i]
        rate['dem2'] = dem[i]
        rate['buy'] = buy[i]
        if len(sel) > i:
            rate['sell_rate'] = sel[i]
        else:
            rate['sell_rate'] = ''
            
        rates.append(rate)
    print(rates)
    
    # rate = []
    # for i in range(len(sel)):
    #     d = {}
    #     c = cur[i]
    #     d['cur'] = c.strip()
    #     if(dem[i].find(' - ') > 0):
    #         if ( dem[i].split(' - ')[0].strip()) > ( dem[i].split(' - ')[1].strip()):
    #             d['dem1']  = dem[i].split(' - ')[1].strip()
    #             d['dem2']  = dem[i].split('-')[0].strip()
    #         else:
    #             d['dem1'] = dem[i].split(' - ')[0].strip()
    #             d['dem2'] = dem[i].split(' - ')[1].strip()
    #     else:
    #         if dem[i] == '':
    #             d['dem1'] = 0
    #             d['dem2'] = 0
    #         else:
    #             d['dem1']  = dem[i].strip()
    #             d['dem2']  = dem[i].strip()
    #     d['buy'] = buy[i].strip()
        
    #     # เช็คว่ามีข้อมูล sell ในรายการหรือไม่ ถ้าไม่มีให้กำหนดค่าว่าง
    #     if i < len(sel):
    #         d['sell'] = sel[i].strip()
    #     else:
    #         d['sell'] = 0
    #     rate.append(d)
    
    # print("d :",d)
    # print("rate :",rate)
   
   
   
    ########################################################################################################
    # หาตารางอัตราแลกเปลี่ยน
    #exchange_table = soup.find('table', {'class': 'text-nowrap nowrap-controller w-100'})
    # สกัดข้อมูลอัตราแลกเปลี่ยนทั้งหมด
    
    # rate = []
    # for row in tr.find_all('tr'):
    #     cols = row.find_all('td')
    #     if len(cols) == 4:
    #         d = {}
    #         # d['cur'] = cols[0].text.strip().replace('\n', '')
    #         # dem_str = cols[1].text.strip().replace('\n', '')
    #         # d['buy'] = cols[2].text.strip().replace('\n', '')
    #         # d['sell'] = cols[3].text.strip().replace('\n', '')
            
    #         c = cur[row]
    #         d['cur'] = cols[0].text.strip()
    #         dem_str = cols[1].dem[row].text.strip()
    #         d['buy'] = cols[2].buy[row].text.strip()
    #         d['sell'] = cols[3].sel[row].text.strip()

    #         # เพิ่มเงื่อนไขให้กับ dem1 และ dem2
    #         if '-' in dem_str:
    #             dem_parts = dem_str.split('-')
    #             d['dem1'] = dem_parts[0].strip()
    #             d['dem2'] = dem_parts[1].strip()
    #         else:
    #              d['dem1'] = dem_str
    #              d['dem2'] = dem_str
    #         #d = {'currency': currency, 'Dem1': dem1, 'Dem2': dem2, 'buy_rate': buy_rate, 'sell_rate': sell_rate}
    # print('d: ',d)
    # print('rate: ',rate)
    
###############################################################################################################
 










    # Prepare the data to update
    
    TWV = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    
    if len(docs) > 0:
    
        # Update the document with the new data
    
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(TWV)
            print(f"Updated document {company_name} with key: {key}")
    else:
    
        # If no document was found, create a new one
    
        db.collection('getCurrency').add(TWV)
        print("Created a new document "+company_name)

    driver.close()
    print('done')


def Rate_K79():
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    company_name = 'K79'
    print("Scraping data "+company_name)
    url = "https://www.k79exchange.com/"
    driver = webdriver.Edge(
        executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
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

    t = tr[3].text.split('\n')

    for x in t:
        if len(x) > 0:
            tmp.append(x)


    final_list = tmp[5:len(tmp)]

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

    rate = []
    rate.append({'agen': company_name})
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
            
    print(d)

    # Prepare the data to update
    K79 = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(K79)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(K79)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def Rate_VSU():
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    company_name = 'VSU'
    print("Scraping data "+company_name)
    url = "http://www.vasuexchange.com/"
    driver = webdriver.Edge(
        executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
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
    for row in tr[5]:
        t = row.text.split('\n')
        for x in t:
            if x != '':
                if x.strip() == 'United States':
                    flag = True
                if flag:
                    final_list.append(x.strip())
    k =0

    currency = ''
    while(1):
        x = final_list[k]
        if(x[0].isdigit() == False):
            if(final_list[k+1][0].isdigit() == False):
                currency = final_list[k+1][0:3]
                cur.append(currency)
                t = final_list[k+1].split(' ')
                if(len(t)>1):
                    dem.append(t[len(t)-1].replace('(','').replace(')','').replace(',',''))
                else:
                    dem.append('0-0')
                buy.append(final_list[k+2])
                sel.append(final_list[k+3])
                k+=3
            else:
                t = final_list[k].split(' ')
                cur.append(t[0][0:3])
                if (len(t) > 1):
                    dem.append(t[len(t) - 1].replace('(', '').replace(')', '').replace(',', ''))
                else:
                    dem.append('0-0')
                buy.append(final_list[k + 1])
                sel.append(final_list[k + 2])
                k += 2

        k+=1
        if k== len(final_list):
            break

    print(len(cur), len(sel), len(dem), len(buy))

    #
    rate = []
    rate.append({'agen': company_name})
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
    print(d)

    # Prepare the data to update
    VSU = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(VSU)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(VSU)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def Rate_XNE():
    
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
    rate.append({'agen': company_name})
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
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(XNE)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(XNE)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def Rate_SME():
    
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    company_name = 'SME'
    print("Scraping data "+company_name)
    url = "http://www.siamexchange.co.th/home/#/"
    driver = webdriver.Edge(
        executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
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
    p =1

    for row in tr:
        td = row.find_all('td')
        for t in td:
            if(len(t.text.strip()) > 0):
                final_list.append(t.text)

    k =0

    currency = ''
    while(1):
        x = final_list[k]
        if(x[0].isdigit() == False):
            currency = final_list[k+1][0:3]
            cur.append(currency)
            t = final_list[k+1].split(' ')
            if(len(t)>1):
                dem.append(t[len(t)-1].replace('(','').replace(')','').replace(',',''))
            else:
                dem.append('0-0')
            buy.append(final_list[k+3])
            sel.append(final_list[k+4])
            k+=4

        k+=1
        if k== len(final_list):
            break

    print(len(cur), len(sel), len(dem), len(buy))


    rate = []
    rate.append({'agen': company_name})
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
            
    print(d)

    # Prepare the data to update
    SME = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(SME)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(SME)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def Rate_VPC():
    
    cred = credentials.Certificate('C:\WebScarp_RateThai\keyFS.json')
    try:
        firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    company_name = 'VPC'
    print("Scraping data "+company_name)
    url = "https://valueplusexchange.com/#/"
    driver = webdriver.Edge(
        executable_path='C:\WebScarp_RateThai\msedgedriver.exe')
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
    rate.append({'agen': company_name})
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
            
    print(d)

    # Prepare the data to update
    VPC = {
        u'agenName': company_name,
        u'agency': rate,
        u'DateTimeUPDATE': str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    }

    # Fetch the document with the matching agenName
    docs = db.collection('getCurrency').where("agenName", "==", company_name).get()

    # Check if a document was found
    if len(docs) > 0:
        # Update the document with the new data
        for doc in docs:
            key = doc.id
            db.collection('getCurrency').document(key).update(VPC)
            print(f"Updated document {company_name} with key: {key}")
    else:
        # If no document was found, create a new one
        db.collection('getCurrency').add(VPC)
        print("Created a new document "+company_name)

    driver.close()
    print('done')

def scrape_data():
    
    Rate_SRO()
    Rate_SRG()
    
    # Rate_TWV() Un handle!?
    
    Rate_K79()
    Rate_VSU()
    Rate_XNE()
    Rate_SME()
    Rate_VPC()
    

# ตั้งเวลาให้รันโค้ด scrape_data() ทุกๆ 24 ชั่วโมง
schedule.every(15).seconds.do(scrape_data)

# วนลูปเพื่อตรวจสอบเวลาและรันโปรแกรมอย่างต่อเนื่อง
while True:
    schedule.run_pending()
    time.sleep(10)  # หยุดรอการตรวจสอบเวลาไว้เป็นระยะๆ
    print("Waiting for next schedule...")






