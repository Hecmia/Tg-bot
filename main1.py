import sqlite3

from urllib.parse import urljoin
from wsgiref.util import request_uri
import re
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS teachers(
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
subjects TEXT,
groups TEXT,
department TEXT,
contacts TEXT
)
''')

con = sqlite3.connect('database0.db')
c0 = con.cursor()

c0.execute('''
CREATE TABLE IF NOT EXISTS linkes(
id INTEGER PRIMARY KEY,
name_0 TEXT NOT NULL,
link 
)
''')
base_url = 'https://pro.guap.ru'
data = {}
for i in range(1, 12):
    page = requests.get('https://pro.guap.ru/professors?position=0&facultyWithChairs=0&subunit=0&fullname=&perPage=100&page=' + str(i))
    soup = BeautifulSoup(page.text, "html.parser")
    links = soup.find('h5', class_= 'mb-sm-1 fw-semibold')

    for h5 in soup.find_all('h5', class_= 'mb-sm-1 fw-semibold'):
        name0 = h5.a.text if h5.a else None
        half_url = h5.a.get('href') if h5.a else None
        full_url = urljoin(base_url, half_url) if half_url else None
        data[str(name0)] = full_url

for key, value in data.items():
    c0.execute('INSERT INTO linkes (name_0, link) VALUES (?, ?)', (key, value,))


#Включить потом:
data_p = {}
c0.execute("SELECT * FROM linkes")
for llink in c0.fetchall():
    page_p = requests.get(f'{llink[2]}')
    soup_p = BeautifulSoup(page_p.text, "html.parser")
    dep = soup_p.find_all(class_='small text-end text-muted mb-1')
    sub = soup_p.find_all(class_='list-group list-group-flush')
    cont = soup_p.find('div', class_='small')
    if dep == "None":
        continue
    for h3 in soup_p.find_all('h3'):
        nam = (h3.text)
    for el1 in dep:
        for el2 in sub:
           for el3 in cont:
               if "@" in el3.text:
                   data_p[str(nam)] = el1.text, el2.text, el3.text, 'None'
               else:
                   el3 = 'Контактов пока нет'
                   data_p[str(nam)] = el1.text, el2.text, el3, 'None'


data_g = {}
#for i in range(1, 752):
for i in range(1, 752):
    if i == 4:
        continue
    page_g = requests.get('https://guap.ru/rasp/?p=' + str(i))
    soup_g = BeautifulSoup(page_g.text, "html.parser")
    gr = soup_g.find_all(class_='groups')
    new_name = ""
    index1 = 0
    index2 = 0
    for h2 in soup_g.find_all('h2'):
        name = h2.text
        for j in range(len(name)):
            if name[j] == "-" and index1 == 0:
                index1 = j
            elif name[j] == "-" and index1 != 0:
                index2 = j
                break
        for k in range(index1+2, index2-4):
            new_name += name[k]
        new_name = new_name.replace(".", " ")
    list_group = ''
    for el_g in gr:
        if el_g.a.text in list_group:
            continue
        list_group += el_g.a.text + " "
        data_g[new_name] = list_group


for key, value in data_p.items():
    for key2, value2 in data_g.items():
        if key2 in key:
            data_p[key] = value[0], value[1], value[2],  value2


for key, value in data_p.items():
    c.execute('INSERT INTO teachers (name, department, subjects, contacts, groups) VALUES (?, ?, ?, ?, ?)', (key, value[0], value[1], value[2], value[3]))


    #print(f'{llink[2]} Ссылка')
#for i in range(1, 752):
#    page_p = requests.get('https://pro.guap.ru/professors/' + str(i))
#    soup_p = BeautifulSoup(page_p.text, "html.parser")
#    dep = soup_p.find_all(class_='small text-end text-muted mb-1')
#    sub = soup_p.find_all(class_='list-group list-group-flush')
#    cont = soup_p.find('div', class_='small')

#    if dep == "None":
#        continue

 #   for h3 in soup_p.find_all('h3'):
#        nam = (h3.text)
 #   for el1 in dep:
 #       #data_p[str(nam)] = el1.text
 #       for el2 in sub:
 #           for el3 in cont:
 #               if "@" in el3.text:
 #                   data_p[str(nam)] = el1.text, el2.text, el3.text
 #               else:
 #                   el3 = 'None'
 #                   data_p[str(nam)] = el1.text, el2.text, el3
        #data_p[str(nam)] = el2.text
            #for el3 in cont:
            #    for h5 in soup_p.find('h5'):
             #       header = h5.text
                #header = el3.find('h5').text.strip()
              #  if header == "Email":
              #      for el4 in em:

                    #email = el3.find('div', class_='small').text.strip()
             #           data_p[str(nam)] = el1.text, el2.text, el4.text
             #   else:
              #      data_p[str(nam)] = el1.text, el2.text, header
#for key, value in data_p.items():
#    c.execute('INSERT INTO articles (name, department, subjects, contacts) VALUES (?, ?, ?, ?)', (key, value[0], value[1], value[2],))



#for key, value in data_p.items():
#    print(key, value)
#print(data_p)
#c.execute('SELECT * FROM articles')
#rows = c.fetchall()
#Выводим данные
#for row in rows:
#    print(row)
con.commit()
con.close()
conn.commit()
conn.close()



