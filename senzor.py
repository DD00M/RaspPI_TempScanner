import socket
import sys
from _thread import *
import time
import csv
from datetime import datetime
import random
from numpy import random as rnd
host = '172.16.31.82'
port = 1233


def ThreadClient (conex):
    y,x=Randxy()
    by="SENZOR "+y+" "+x
    conex.send(bytes(by,encoding='utf-8'))
    Nume=conex.recv(1024)
    NumeF=str(Nume)
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(10)
        Input = #aicitemperatura+";"+current_time
        conex.send(str.encode(Input))
        print (NumeF+" a trimis un mesaj de TEST!")
        #Response = ClientSocket.recv(2048)
        #print(Response.decode('utf-8'))
    conex.close()


ClientSocket= socket.socket()
try:
        ClientSocket[i].connect((host, port))
except socket.error as e:
        print(str(e))
        print ('Se inchide programul...')
        sys.exit()
ThreadClient(ClientSocket)

