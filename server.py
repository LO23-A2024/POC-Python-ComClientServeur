import tkinter as tk
import socket
import threading
import time
import select

start = False
listenThread = None
s = None
listConn = list()

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
    global listConn
    global s
    eventStop.clear()
    addr = ("localhost", 8080)
    s = socket.create_server(addr)
    s.listen()
    s.setblocking(0)
    listConn.append(s)
    listenThread = threading.Thread(target=listen)
    listenThread.start()


def listen():
    global s
    global listConn
    global eventStop
    while not eventStop.is_set():
        ready_to_read, ready_to_write, in_error = select.select(listConn,listConn,listConn,0.5)
        for socket in ready_to_read:
            if socket == s :
                conn, addr = socket.accept()
                print(addr)
                listConn.append(conn)
            else:
                data = socket.recv(1024)
                print(data.decode('ascii'))
                socket.send(data)



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
