import tkinter as tk
import socket
import threading
import time
import select

class UI: 

    def __init__(self, callbackStart, callbackStop):
        self.window = tk.Tk()
        self.bt = tk.Button(text ="Start", command = self.buttonClick)
        self.bt.pack()
        self.callbackStart = callbackStart
        self.callbackStop = callbackStop
        self.start = False

    def run(self):
        self.window.mainloop()

    def buttonClick(self):
        if self.start:
            print("Stop")
            self.callbackStop()
            self.bt.config(text="Start")
        else:
            print("Start")
            self.callbackStart()
            self.bt.config(text="Stop")
        self.start = not self.start


class Server:

    def __init__(self):
        self.start = False
        self.serverSocket = None
        self.listConn = []
        self.eventStop = threading.Event()
        self.eventStop.clear()


    def stopServer(self):
        self.eventStop.set()
        time.sleep(2)
        self.serverSocket.close()
        self.serverSocket = None

    def startServer(self):
        self.eventStop.clear()
        addr = ("localhost", 8080)
        self.serverSocket = socket.create_server(addr)
        self.serverSocket.listen()
        self.serverSocket.setblocking(0)
        self.listConn.append(self.serverSocket)
        listenThread = threading.Thread(target=self.listen)
        listenThread.start()


    def listen(self):
        while not self.eventStop.is_set():
            ready_to_read, ready_to_write, in_error = select.select(self.listConn, self.listConn, self.listConn, 1.0)
            for socket in ready_to_read:
                if socket == self.serverSocket :
                    conn, addr = socket.accept()
                    print(addr)
                    self.listConn.append(conn)
                else:
                    data = socket.recv(1024)
                    print(data.decode('ascii'))
                    socket.send(data)




def main():
    s = Server()
    interface = UI(s.startServer, s.stopServer)
    
    interface.run()
    

if __name__ == '__main__':
    main()
