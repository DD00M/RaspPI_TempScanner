from flask import Flask
from flask import sessions
from flask import request
from flask import render_template
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import socket


app = Flask(__name__)



@app.route('/')
def index():
    print('CEVA TEST!')
    return render_template('TempScanner.html')


@app.route('/start.html')
def ceva():
   # echo-client.py
    import socket
    import time

    HOST = "172.16.31.82"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server
    data=""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        time.sleep(0.2)
        data = s.recv(1024)
        print(f"Received {data!r}")

    site="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\"><head><title>TempScanner</title><link href=\"../static/css/aspect.css\" rel=\"stylesheet\" type=\"text/css\" /></head><body><nav><div class=\"Logo\" style=\"font-size:30px\">TempCheck</div><div class=\"Img_Div\"><img src=\"../static/images/termo2.png\"></div> <div class=\"banane\">"
    site2="</div></nav><div class=\"Footer\"><p>Proiect realizat de sd. cap. Dumitrascu Andrei-Cosmin si sd. cap. Mitran Luca-Radu la Academia Tehnica Militara \"Ferdinand I\", Bucuresti - 2022</p></div></body></html>"
    text_html="<b> Temperatura este "
    text_html+=data.decode()
    text_html+=" grade Celsius. </b>"
    site+=text_html
    site+=site2
    print(f"Received {data!r}")
    return site



if __name__  == "__main__":
    app.run(debug=True)





