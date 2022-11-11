import datetime
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

html_txt = requests.get('http://evaluare.edu.ro/Evaluare/CandPerScoalaIAD.aspx?Jud=11&Sc=11350856').text
#print(html_txt)

soup = BeautifulSoup(html_txt, 'lxml')

lic_bz=soup.find_all('td', class_="td1", nowrap='nowrap')
count=0
for i in lic_bz:
    print(i.prettify())
    count+=1
print("numarul de elevi din hasdeu este: "+str(count))