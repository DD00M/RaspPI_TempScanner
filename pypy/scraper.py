import datetime
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

html_txt = requests.get('https://vremea.ido.ro/Bucuresti.htm').text
#print(html_txt)

soup = BeautifulSoup(html_txt, 'lxml')
tags = soup.find('div', id="now")
zi = soup.find('div', id="cal")
#print(tags.prettify())
#print(zi.prettify())

translator = Translator()
now = datetime.datetime.now()
aux = now.strftime("%A")
now_translated = translator.translate(aux, src='en', dest='ro')
print(now_translated.text)

count1 = 0
check_day=""

for i in zi:
    if count1 == 0:
        #print(i)
        check_day=i
    count1+=1

if check_day.find(now_translated.text):
    print("ziua este corecta")

count = 0

text_actual=""

for i in tags:
    if i == "Temperatura acum: ":
        count = 0
    else:
        count+=1
    if count == 1:
        #print(i)
        text_actual=i

temp=text_actual.text.split('><')
print(temp)

temperatura_actuala=temp[0][0:2]
print(temperatura_actuala)

#if temp[0] == "25°C":
#   print("gata")

#print(html_txt.find("Temperatura acum: "))
"""
with open('TempScanner.html','r') as html_file:
    content = html_file.read()
    #print(content)
    soup = BeautifulSoup(content, 'lxml')
    #print(soup.prettify())
    #divs_tags = soup.find_all('div')   
    #print(tags)
    #for i in divs_tags:
    #    print(i.text)
    translator = Translator()
    now = datetime.datetime.now()
    aux = now.strftime("%A")
    now_translated = translator.translate(aux, src='en', dest='ro')
    print(now_translated.text)
    temperatura = soup.find('h2', class_='date')
    #for i in temperatura:
"""
