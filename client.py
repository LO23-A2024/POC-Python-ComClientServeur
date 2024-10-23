import tkinter as tk
import socket
import threading
import select

listening = False
sending = False

def createSocket():
    global s
    s = createSocket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 8080
    s.connect((host, port))
    t1 = threading.Thread(target=listen, args=[s])
    t1.start()

def ButtonClick():
    global sending
    sending = True

def ButtonConnect():
    global sending
    sending = True


def connect():
    global s
    global lb
    print("Sending")
    s.send(lb.get().encode('ascii'))


def listen(s):
    global sending
    global lb
    while True:
        ready_to_read, ready_to_write, in_error = select.select([s],[s],[s],1.0)
        if sending :
            for socket in ready_to_write :
                socket.send(lb.get().encode('ascii'))

        for socket in ready_to_read:
            if data:
                data = socket.recv(1024)
                lb.config(text="Données reçues : " + data.decode('ascii'))
            else :
                print("Connection closed")


def main():
    global lb
    window = tk.Tk()
    data=tk.StringVar()
    inp = tk.Entry(textvariable = data, font=('calibre',10,'normal'))
    btSend = tk.Button(text="Send", command = ButtonClick)
    btConnect = tk.Button(text="Start connection", command = createSocket)
    lb = tk.Label(text="Données reçues : ", font=('calibre',10, 'bold'))
    inp.pack()
    btSend.pack()
    btConnect()
    lb.pack()
    createSocket()
    window.mainloop()
