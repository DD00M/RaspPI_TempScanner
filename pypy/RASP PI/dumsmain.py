from concurrent.futures import thread
from flask import Flask
from flask import sessions
from flask import request
from flask import render_template
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import requests
import socket
import _thread
#from main import next

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import datetime
#from main import next
def scraper1():
    

    html_txt = requests.get('https://vremea.ido.ro/Bucuresti.htm').text
    #  print(html_txt)

    soup = BeautifulSoup(html_txt, 'lxml')
    tags = soup.find('div', id="now")
    zi = soup.find('div', id="cal")
    #print(tags.prettify())
    #print(zi.prettify())

    translator = Translator()
    now = datetime.datetime.now()
    aux = now.strftime("%A")
    now_translated = translator.translate(aux, src='en', dest='ro')
    #print(now_translated.text)

    count1 = 0
    check_day=""

    for i in zi:
     if count1 == 0:
        #print(i)
        check_day=i
     count1+=1

    #if check_day.find(now_translated.text):
     #print("ziua este corecta")

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
    #print(temp)

    temperatura_actuala=temp[0][0:2]
    #print(temperatura_actuala)
    return temperatura_actuala
def scraper2():
    #https://weather.com/ro-RO/weather/tenday/l/Bucure%C8%99ti+Bucure%C8%99ti?canonicalCityId=09ab35eae00f21604b305d3aa496ff31777f8979cf6cfa560e1dd22133813806


    html_txt = requests.get('https://www.vremea.com/vremea-bucuresti/LRBS').text
    #print(html_txt)

    soup = BeautifulSoup(html_txt, 'lxml')
    tags = soup.find('div', {'class': 'tempcurent'})
    stare = soup.find('td', class_="underline hidecol")
    #print(tags)
    print(stare)
    
    count=0
    temp_actual=""
    for i in tags:
        if i.find("ANM") != -1:
            temp_actual=temp_actual+i.text

    txt=stare.text.split('><')
    #print(txt[0].encode('utf8'))
    #print(temp_actual)
    return temp_actual

def scraper3():

    html_txt = requests.get('https://freemeteo.ro/vremea/bucharest/starea-vremii/locatie/?gid=683506&language=romanian&country=romania').text
    #print(html_txt)

    soup = BeautifulSoup(html_txt, 'lxml')
    tags = soup.find('div', class_="temp")
    mod = soup.find('div', class_="pred")
    #print(tags.prettify())
    print(mod.prettify())

    count=0
    temp=0

    for i in tags:
        temp=i
        break

    return temp

app = Flask(__name__)

@app.route('/')
def index():
    print('CEVA TEST!')
    return render_template('TempScanner.html')

@app.route('/start.html')
def ceva():
    import socket
    import time

    HOST = "172.16.4.21"  # The server's hostname or IP address
    PORT = 1233  # The port used by the server
    data=""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(b"CLIENT")
        time.sleep(0.2)
        data = s.recv(1024)
        print(f"Received {data!r}")
        string=str(data)
        medie=string.split()
        print (medie[1])
        format_float = "{:.2f}".format(float(medie[1]))
    i=0
    site="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /><link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"></head><body><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><nav class=\"lista_site\"><ul><li><a href=\"https://vremea.ido.ro/Bucuresti.htm\">www.vremea.ido.ro</a></li></br><p style=\"font-family:Arial, Helvetica, sans-serif; color:white; size: 50px; position:relative; top:12px\">"
    temp1=scraper1()
    site+=temp1
    site+="°C"
    site+="</p><li><a href=\"https://www.vremea.com/vremea-bucuresti/LRBS\">www.vremea-bucuresti.com</a></li></br><p style=\"font-family:Arial, Helvetica, sans-serif; color:white; size: 50px; position:relative; top:12px\">"
    temp2=scraper2()
    site+=temp2
    site+= "</p><li><a href=\"https://freemeteo.ro/vremea/bucharest/starea-vremii/locatie/?gid=683506&language=romanian&country=romania\">www.freemeteo.ro</a></li></br><p style=\"font-family:Arial, Helvetica, sans-serif; color:white; size: 50px; position:relative; top:12px\">"
    temp3=scraper3()
    site+=temp3
    site+="°C"
    site+= "</p></ul><form method=\"post\" action=\"/\"><input class=\"casuta1\" value=\"\" name=\"casuta1\" style=\"color:white\"/><input class=\"casuta2\" value=\"\" name=\"casuta2\" style=\"color:white\"/><input class=\"casuta3\" value=\"\" name=\"casuta3\" style=\"color:white\"/></form></nav><div class=\"temps\">Temperatura medie inregistrata de senzori este : "
    site+=str(format_float)
    string.replace(" "," grade C,")
    site+="°C"
    site+="<div class=\"Ltemps\"><p>Numarul de senzori este:  "
    copieVector=medie
    nr=medie[0].split("'")
    site+= nr[1]
    site+= "</p>"
    site+= "</br><p> Temperaturile primite de la senzori sunt: "
    #numar=int(medie[0])
    count=0
    for i in copieVector:
        if count>1:
            i.replace("'", " ")
            site+= str(i)
            site+= "°C"
            site+=" "
        count+=1
    site+= "</p></div>"
    site+= " </div><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div></body></html><div class=\"banane\">"
    
    site2="</div></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div></body></html>"
    #text_html="<b> Temperatura este "
    #text_html+=data.decode()
    #text_html+=" grade Celsius. </b>"
    #site+=text_html
    #site+=site2
    #print(f"Received {data!r}")
 
    return site


@app.route('/TempScanner.html')
def func():
    site="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"> <html xmlns=\"http://www.w3.org/1999/xhtml\"> <head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /> <link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"></head> <body> <nav class=\"menu\"> <div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"> </div> <ul> <li><a href=\"TempScanner.html\">Home</a></li> <li><a href=\"about_us.html\">About Us</a></li> <li><a href=\"contact.html\">Contact</a></li>  <li><a href=\"start.html\">Start App</a></li> </ul> </nav> <div class=\"Footer\"> <p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p> </div> </body> </html> "
    return site

@app.route('/about_us.html')
def func2():
    site='<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /> <link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"> </head><body><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div><div class=\"Chenar2\"><p style=\"color:aliceblue\"></t>Buna ziua! Aceasta aplicatie este dezvoltata pe timpul practicii de catre studentii Dumitrascu Andrei-Cosmin si Mitran Luca-Radu. Scopul aplicatiei este de a face o statistica asupra temperaturilor din mediul inconjurator.</p></br><p style=\"color:aliceblue\"> De asemenea aceste temperaturi obtinute vor fi verificate si comparate cu datele de pe site-urile specializate pentru comunicarea temperaturii actuale.</p></br><p style=\"color:aliceblue\"> Pe langa statistica temperaturilor, se pot oferi recenzii site-urilor disponibile pentru a putea stabili care informatie este credibila.</p></div></body>'
    return site

@app.route('/contact.html')
def func3():
    site='<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /> <link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"> </head><body><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara "Ferdinand I", Bucuresti - 2022</p></div><div class=\"Chenar1\"><p style=\"color:aliceblue\">EMAIL</p></br><p style=\"color:aliceblue\">Sd. Cap. Dumitrascu Andrei-Cosmin: andrei.dumitrascu@mta.ro</p></br><p style=\"color:aliceblue\">Sd. Cap. Mitran Luca-Radu: luca.mitran@mta.ro</p> </br><p style=\"color:aliceblue\">NUMAR DE TELEFON</p></br><p style=\"color:aliceblue\">Sd. Cap. Dumitrascu Andrei-Cosmin: 0784656365</p></br><p style=\"color:aliceblue\">Sd. Cap. Mitran Luca-Radu: 0749128588</p></div></body>'
    return site

if __name__  == "__main__":
    #_thread.start_new_thread(ceva, ())
    #_thread.start_new_thread(next, ())
    app.run(debug=True)





