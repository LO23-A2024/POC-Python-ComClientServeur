import tkinter as tk
import socket
import threading
import time

start = False
t1 = None
t2 = None
s = None
list = list()
eventStop = threading.Event()
eventStop.clear()

def message(reader, writer):
    print(reader, writer)

def stopServer():
    global s
    global eventStop
    eventStop.set()
    time.sleep(1)
    s.close()
    s = None

def startServer():
    global s
    eventStop.clear()
    addr = ("localhost", 8080)
    s = socket.create_server(addr)
    socketServer = s
    t1 = threading.Thread(target=acceptConnection, args=[s])
    t1.start()
    t2 = threading.Thread(target=listen)
    t2.start()

def acceptConnection(s):
    global list
    global eventStop
    while not eventStop.is_set():
        conn, addr = s.accept()
        print(addr)
        list.append(conn)

def listen():
    global list
    global eventStop
    while not eventStop.is_set():
        try:
            for conn in list:
                data = conn.recv(1024)
                print(data.decode('ascii'))
                conn.send(data)
        except:
            pass

def ButtonClick():
    global start
    if start:
        print("Stop")
        stopServer()   
        bt.config(text="Start")
    else:
        print("Start")
        startServer() 
        bt.config(text="Stop")
    start = not start


def main():
    window = tk.Tk()
    global bt
    bt = tk.Button(text ="Start", command = ButtonClick)
    bt.pack()
    window.mainloop()
    

if __name__ == '__main__':
    socketServer = None
    main()
