from concurrent.futures import thread
from flask import Flask
from flask import sessions
from flask import request
from flask import render_template , session
from flask import redirect, url_for, g
from werkzeug.utils import secure_filename
import json
import os
import requests
import socket
import _thread
import datetime
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import hashlib
import csv
from csv import reader
from PIL import Image
#from main import next

LOGGED=False


def map(lista1,lista2):
    img = Image.open('romania.png')
    pixels = img.load() # create the pixel map

    prima=0.00307853 
    doua=0.00456335
    colt1=48.28579
    colt2=19.92

   
    for k in range(len(lista1)):
        lista1[k]=colt1-float(lista1[k])
        lista2[k]=-colt2+float(lista2[k])
        
        lista1[k]=int(lista1[k]/prima)
        lista2[k]=int(lista2[k]/doua)

        #print(lista1[k])
        #print(lista2[k])
    var=10
    for k in range(len(lista1)):
     for i in range(22):
        for j in range(22):
            if lista1[k]+i-11<1550 and lista1[k]+i-11>0 and lista2[k]+j-11>0 and lista2[k]+j-11<2190:
                pixels[lista2[k]+j-1,lista1[k]+i-11] = (15, 239-int(var), 247)
                var+=1
                var=var%239
    img.save('./static/images/map.png')

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    def get_name(self):
        return self.username
    def __repr__(self):
        return f'<User: {self.username}>'

app = Flask(__name__)
filename="logs.csv"

def logger(name , passw):
   
    in_file = open(filename, "r")
    csv_reader = reader(in_file)
    row_count = sum(1 for row in csv_reader)
    ses=row_count+1
    in_file.close()
    out_file = open(filename, "a")
    writer = csv.writer(out_file,delimiter=" ")
    
    rand=[]
    rand.append(name)
    passw = hashlib.md5(passw.encode())
    rand.append(passw.hexdigest())
    rand.append(ses)
    #print (rand)
    writer.writerow(rand)
    out_file.flush()
    out_file.close()
    
def find_me(name,passw):
    in_file = open(filename, "r")
    csv_reader = reader(in_file)
    password = hashlib.md5(passw.encode())
    password=password.hexdigest()
    for row in csv_reader:
        if len(row):
           
            string= str(row[0])
            user_nou=string.split()
            user=(User(id=int(user_nou[2]), username=user_nou[0], password=user_nou[1]))
            if user.username == name and user.password==password:
                return user
    return False
   
def find_me_by_ID(ID):
    in_file = open(filename, "r")
    csv_reader = reader(in_file)
    for row in csv_reader:
        if len(row):
            string= str(row[0])
            user_nou=string.split()
            user=(User(id=int(user_nou[2]), username=user_nou[0], password=user_nou[1]))
            if user.id==ID:
                return user
    return False

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

    #print(temp)
    count=0
    temp_actual=""
    for i in tags:
        if i.find("ANM") != -1:
            temp_actual=temp_actual+i.text

    #txt=stare.text.split('><')
    #print(txt[0].encode('utf8'))
    print(temp_actual)
    return temp



app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    #session.pop('user_id', None)

    if 'user_id' in session:
        
        #for cont in users:
            #if cont.id == session['user_id']:
            g.user = find_me_by_ID(session['user_id'])
                
        
#ERROR=-1
@app.route('/sign', methods=['GET', 'POST'])
def sign():
    global LOGGED
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['usrname']
        password = request.form['password']

        if len(username)==0:
            return render_template('signup.html')
        print(username+password)
        #ADD ME IN FILE
        logger(username,password)
        user=find_me(username,password)
        session['user_id'] = user.id
        LOGGED=True
        return redirect(url_for('profile'))
    return render_template('signup.html')
        #ERROR=0

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    #global ERROR
    #print ("Error is: "+str(ERROR))
    global LOGGED
    if request.method == 'POST':
        session.pop('user_id', None)
       

        username = request.form['usrname']
        password = request.form['password']

        if len(username)==0:
            return render_template('login.html')
        print(username+password)
        #for cont in users:
            #if cont.username == username:
                #user = cont 
                #if user and user.password == password:
                    #session['user_id'] = user.id
                    #ERROR=1
        result=find_me(username,password)
        if result!=False:
            session['user_id']=result.id
            LOGGED=True
            return redirect(url_for('profile'))
        #ERROR=0

        return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    global LOGGED
    if LOGGED== False:
         return render_template('retroerror.html')
    if request.method == 'POST':
         session.pop('user_id', None)
         LOGGED=False
         return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/retroerror')
def error():
    return render_template('retroerror.html')


@app.route('/redirect', methods=['GET', 'POST'])
def log():

     if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['usrname']
        password = request.form['password']
        print(username+password)
        #for cont in users:
            #if cont.username == username:
                #user = cont 
                #if user and user.password == password:
                    #session['user_id'] = user.id
                    #ERROR=1
        result=find_me(username,password)
        if result!=False:
            session['user_id']=result.id
            return redirect(url_for('profile'))
        #ERROR=0

        return redirect(url_for('login'))
     else:
         return render_template('login.html')

@app.route('/')
def index():
    g.user=None
    #session.pop('user_id', None)
    print('CEVA TEST!')
    return redirect(url_for('login'))

@app.route('/start.html')

def ceva():
    global LOGGED
    if LOGGED== False:
         return render_template('retroerror.html')
    import socket
    import time

    HOST = "172.16.31.82"  # The server's hostname or IP address
    PORT = 1233  # The port used by the server
    data=""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(b"CLIENT x x")
        time.sleep(0.2)
        data = s.recv(2048)
        list1=s.recv(2048)
        list2=s.recv(2048)
        print(list1)
        print(list2)
        print(f"Received {data!r}")
        string1=str(data)
        string=string1.split('x')[0]

        locx=string1.split('x')[1]
        locy=string1.split('x')[2]

        listax=locx.split()
        listay=locy.split()
        print(listax)
        print(listay)
        map(listax,listay)
        medie=string.split()
        print (medie[1])
        format_float = "{:.2f}".format(float(medie[1]))
    i=0
    site="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /><link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"></head><body scroll=\"nu\" style=\"overflow:hidden\"><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><nav class=\"lista_site\"><ul><li><a href=\"https://vremea.ido.ro/Bucuresti.htm\">www.vremea.ido.ro</a></li></br><p style=\"font-family:Arial, Helvetica, sans-serif; color:white; size: 50px; position:relative; top:12px\">"
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
    site+= "</p></ul><form method=\"post\" action=\"/\"><button class=\"like1\"></button><button class=\"like2\"></button><button class=\"like3\"></button><button class=\"dislike1\"></button><button class=\"dislike2\"></button><button class=\"dislike3\"></button></form></nav><div class=\"temps\">Temperatura medie inregistrata de senzori este : "
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
    site+= ""
    site+= " </div><div class=\"abc\"><img src=\"./static/images/map.png\" width=\"580\" height=\"370\"></div><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div></body scroll=\"nu\" style=\"overflow:hidden\"></html><div class=\"banane\">"
    
    site2="</div></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div></body scroll=\"nu\" style=\"overflow:hidden\"></html>"
    #text_html="<b> Temperatura este "
    #text_html+=data.decode()
    #text_html+=" grade Celsius. </b>"
    #site+=text_html
    #site+=site2
    #print(f"Received {data!r}")
 
    return site

@app.route('/TempScanner.html', methods=['GET', 'POST'])
def func():
    global LOGGED
    if LOGGED== False:
         return render_template('retroerror.html')
    if  request.method == 'POST':
        g.user=None
        LOGGED=False
        return redirect(url_for('login'))
    return render_template('TempScanner.html')

@app.route('/about_us.html')
def func2():
    global LOGGED
    if LOGGED== False:
         return render_template('retroerror.html')
    site='<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /> <link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"> </head><body scroll=\"nu\" style=\"overflow:hidden\"><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div><div class=\"Chenar2\"><p style=\"color:aliceblue\"></t>Buna ziua! Aceasta aplicatie este dezvoltata pe timpul practicii de catre studentii Dumitrascu Andrei-Cosmin si Mitran Luca-Radu. Scopul aplicatiei este de a face o statistica asupra temperaturilor din mediul inconjurator.</p></br><p style=\"color:aliceblue\"> De asemenea aceste temperaturi obtinute vor fi verificate si comparate cu datele de pe site-urile specializate pentru comunicarea temperaturii actuale.</p></br><p style=\"color:aliceblue\"> Pe langa statistica temperaturilor, se pot oferi recenzii site-urilor disponibile pentru a putea stabili care informatie este credibila.</p></div></body>'
    return site

@app.route('/contact.html')
def func3():
    global LOGGED
    if LOGGED== False:
         return render_template('retroerror.html')
    site='<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /> <link rel=\"icon\" href=\"../static/images/termo2.png\" type=\"image/x-icon\"> </head><body scroll=\"nu\" style=\"overflow:hidden\"><nav class=\"menu\"><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div><ul><li><a href=\"TempScanner.html\">Home</a></li><li><a href=\"about_us.html\">About Us</a></li><li><a href=\"contact.html\">Contact</a></li><li><a href=\"start.html\">Start App</a></li></ul></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara "Ferdinand I", Bucuresti - 2022</p></div><div class=\"Chenar1\"><p style=\"color:aliceblue\">EMAIL</p></br><p style=\"color:aliceblue\">Sd. Cap. Dumitrascu Andrei-Cosmin: andrei.dumitrascu@mta.ro</p></br><p style=\"color:aliceblue\">Sd. Cap. Mitran Luca-Radu: luca.mitran@mta.ro</p> </br><p style=\"color:aliceblue\">NUMAR DE TELEFON</p></br><p style=\"color:aliceblue\">Sd. Cap. Dumitrascu Andrei-Cosmin: 0784656365</p></br><p style=\"color:aliceblue\">Sd. Cap. Mitran Luca-Radu: 0749128588</p></div></body scroll=\"nu\" style=\"overflow:hidden\">'
    return site


if __name__  == "__main__":
    #_thread.start_new_thread(ceva, ())
    #_thread.start_new_thread(next, ())
    app.run(debug=True)


