import tkinter as tk
import socket
import time

def createSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost' 
    port = 8080
    s.connect((host, port))
    return s

def ButtonClick():
    global s
    global data
    global lb
    print("Sending")
    s.send(data.get().encode('ascii'))
    print("Waiting for response")
    d = s.recv(1024)
    lb.config(text=d.decode('ascii'))


s = createSocket()
window = tk.Tk()
data=tk.StringVar()
inp = tk.Entry(textvariable = data, font=('calibre',10,'normal'))
bt = tk.Button(text="Send", command = ButtonClick)
lb = tk.Label(text="Test", font=('calibre',10, 'bold'))
inp.pack()
bt.pack()
lb.pack()
window.mainloop()
