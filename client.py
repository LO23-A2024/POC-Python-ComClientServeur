import tkinter as tk
import socket
import threading

t1 = None
listC = list()

def createSocket():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost' 
    port = 8080
    s.connect((host, port))
    global t1
    t1 = threading.Thread(target=listen)
    t1.start()
    return s

def ButtonClick():
    global s
    global data
    global lb
    print("Sending")
    s.send(data.get().encode('ascii'))


def listen():
    global listC
    global s
    while True:
        d = s.recv(1024)
        print(d.decode('ascii'))
        for i in listC:
            i(d)
        

def callbackCall(data):
    global lb
    lb.config(text=data.decode('ascii'))


s = createSocket()
window = tk.Tk()
data=tk.StringVar()
listC.append(callbackCall)
inp = tk.Entry(textvariable = data, font=('calibre',10,'normal'))
bt = tk.Button(text="Send", command = ButtonClick)
lb = tk.Label(text="Test", font=('calibre',10, 'bold'))
inp.pack()
bt.pack()
lb.pack()
window.mainloop()
