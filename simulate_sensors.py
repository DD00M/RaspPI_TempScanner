import socket
import sys
from _thread import *
import time
import csv
from datetime import datetime
import random
host = '192.168.3.75'
port = 1233


def RandTemp():
    return str(random.randint(20,30))


#Response = ClientSocket.recv(2048)
def ThreadClient (conex):
    conex.send(b'SENZOR')
    Nume=conex.recv(1024)
    NumeF=str(Nume)
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(10)
        Input = RandTemp()+";"+current_time
        conex.send(str.encode(Input))
        print (NumeF+" a trimis un mesaj de TEST!")
        #Response = ClientSocket.recv(2048)
        #print(Response.decode('utf-8'))
    conex.close()

numar=int(input('Introdu numarul de senzori: '))
ClientSocket= [socket.socket] * numar
for i in range(numar):
    ClientSocket[i]= socket.socket()
    try:
        ClientSocket[i].connect((host, port))
    except socket.error as e:
        print(str(e))
        print ('Se inchide programul...')
        sys.exit()


for i in range(numar):
    print (f'Simulez senzorul {i}')
    time.sleep(0.1)
    print(f'Thread {i} a inceput')
    start_new_thread(ThreadClient, (ClientSocket[i], ))
