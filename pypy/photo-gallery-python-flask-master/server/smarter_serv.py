import socket
from _thread import *
import csv
import time
from csv import reader

host = '172.16.4.21'
port = 1233
ThreadCount = 0
senzori=0
Nume='Senzor'
counter=-1
w, h = 1000, 50
Matrix = [['x' for x in range(w)] for y in range(h)]



def temps():
    total_list=[]
    ultimele=[]
    medie=0
    numar=0
    with open('out.csv', 'r') as read_obj:
     csv_reader = reader(read_obj)
     
     for row in csv_reader:
        #print (row)
        if len(row):
            string=row[0]
            list=string.split('x',1)
            temperatu=list[0].split()
            temperaturi=[]
            for item in temperatu:
                item2=item.split(";")
                temperaturi.append(item2[1])
            #print (temperaturi)
            if len(temperaturi):
                #print(temperaturi)
                total_list+=temperaturi
                #print(temperaturi [-1])
                ultimele.append(temperaturi[-1])
    if len(total_list):
     for temp in total_list:
        numar+=1
        medie+=float(temp)
    medie=medie/numar
    return total_list,ultimele,medie

def client_handler(connection):
    global counter
    global Matrix
    global senzori
    #print (counter)
    myID=counter+1
    counter=counter+1
    
    NumeF=Nume+str(counter)
    #Matrix[counter][0]=NumeF
    #print (NumeF)
    #TREBUIE FACUT UN RECV PENTRU A FACE
    #DIFERENTA DINTRE SENZORI SI CLIENTI
    Type=""
    Type=connection.recv(1024)
    print(Type)
   
    j=0
    
    if Type==b'SENZOR':
     connection.send(str.encode(NumeF))
     senzori+=1
     while True:
        
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message == 'BYE':
            break
        #reply = f'Server: {message}'
        mesajF=NumeF+";"+message
        print (mesajF)
        Matrix[myID][j]=mesajF
        j=j+1
        #connection.sendall(str.encode(reply))
    if Type==b'CLIENT':
        mesaj=str(senzori)
        mesaj+=" "
        total,ultim,medie=temps()
        mesaj+=str(medie)
        mesaj+=" "
        for item in ultim:
            mesaj+=str(item)
            mesaj+=" "
        #print (bytes(mesaj,encoding='utf-8'))
        connection.send(bytes(mesaj,encoding='utf-8'))

    connection.close()

def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (Client, ))
''
def writeMe(cv):
    global writer
    while True:
        time.sleep(15)
        out_file = open("out.csv", "w")
        writer = csv.writer(out_file,delimiter=" ")
        print("Scriu")
        for row in Matrix:
            #print (row)
            #print ('next')
            writer.writerow(row)
            out_file.flush()
        print("Safe")
def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()
    start_new_thread(writeMe,(0,))
    while True:
        accept_connections(ServerSocket)


start_server(host, port)
