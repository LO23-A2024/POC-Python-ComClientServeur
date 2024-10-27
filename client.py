from tkinter import *
import socket
import threading
import select




class UI:
    def __init__(self):
        self.window = Tk()

        self.labelInfo = Label(text="Info/Erreurs : Aucune connection", font=('calibre',10, 'bold'))
        self.btConnect = Button(text="Start connection")

        self.dataInput= StringVar()
        self.input = Entry(textvariable = self.dataInput, font=('calibre',10,'normal'))
        self.btSend = Button(text="Send")
        self.labelData = Label(text="Données reçues : ", font=('calibre',10, 'bold'))
        
        self.labelInfo.pack()
        self.btConnect.pack()
        self.input.pack()
        self.btSend.pack()
        self.labelData.pack()


    def run(self):
        self.window.mainloop()

    def setConnect(self, func):
        self.btConnect.config(command=func)

    def setSend(self, func):
        self.btSend.config(command= lambda: func(self.dataInput.get()))

    def setInfo(self, infoStr):
        self.labelInfo.config(text="Info/Erreurs :" + infoStr)

    def setData(self, dataStr):
        self.labelData.config(text="Info/Erreurs :" + dataStr)






class ClientSocket:
    
    host = 'localhost'
    port = 8080

    def __init__(self, callbackInfo, callbackData):
        self.callbackInfo = callbackInfo
        self.callbackData = callbackData
        self.message = None
        self.socket = None

    def connect(self):
        try:
            if self.socket is not None:
                self.socket.close()
            else :
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ClientSocket.host, ClientSocket.port))
        except Exception as ex:
            self.callbackInfo(str(ex))
        else:
            self.callbackInfo("Connection effectué")
            t = threading.Thread(target=self.listen, args=[])
            t.start()

    def listen(self):
        
        while self.socket is not None:
            ready_to_read, ready_to_write, in_error = select.select([self.socket],[self.socket],[self.socket],1.0)
            
            if self.message is not None :
                print("test")
                for socket in ready_to_write :
                    try:
                        socket.send(self.message.encode('ascii'))
                    except Exception as ex:
                        self.callbackInfo(str(ex))
                    self.message = None

            for socket in ready_to_read:
                try :
                    data = socket.recv(1024)
                    if data:
                        self.callbackData(data.decode('ascii'))
                    else :
                        self.callbackInfo("socket fermé")
                        self.socket = None
                except Exception as ex :
                    self.callbackInfo(str(ex))

            for socket in in_error:
                print("Erreur")
                socket.close()
                self.socket = None
                

    def sendData(self, data):
        self.message = str(data)







def main():
    interface = UI()
    s = ClientSocket(interface.setInfo, interface.setData)
    interface.setConnect(s.connect)
    interface.setSend(s.sendData)
    interface.run()




if __name__ == '__main__':
    main()