import socket
import threading
import select
import time
import json
import random
import string


class ClientSocket:
    
    host = 'localhost'
    port = 8080

    def __init__(self):
        self.callbackMessageRecu = None
        self.message = None
        self.socket = None
        self.eventStop = threading.Event()
        self.eventStop.clear()

    def setCallbackMessageRecu(self, func):
        self.callbackMessageRecu = func

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ClientSocket.host, ClientSocket.port))
        print("Connection effectué")
        t = threading.Thread(target=self.listen, args=[])
        t.start()

    def listen(self):

        while not self.eventStop.is_set():

            #Check flags des sockets            
            ready_to_read, ready_to_write, in_error = select.select([self.socket],[self.socket],[self.socket],1.0)
            
            #Envoie
            if self.message is not None :
                for socket in ready_to_write :
                    try:
                        #Test envoie json
                        dict = {"message": self.message, "randomData": "ilconnaitpasRaoul"}
                        data = json.dumps(dict)
                        socket.send(bytes(data, encoding="utf-8"))
                    except Exception as ex:
                        print(str(ex))
                        self.eventStop.set()
                    self.message = None

            #Réception
            for socket in ready_to_read:
                try :
                    data = socket.recv(1024)
                    if data:
                        self.callbackMessageRecu(data.decode("utf-8"))
                    else :
                        print("socket fermé")
                        self.socket = None
                        self.eventStop.set()
                except Exception as ex :
                    print(str(ex))
                    self.eventStop.set()

            #En cas d'erreur
            for socket in in_error:
                print("Erreur")
                socket.close()
                socket = None
                self.eventStop.set()
                

    def sendData(self, str_data):
        self.message = str_data

    def close(self):
        try : 
            self.eventStop.set()
            time.sleep(2)
            self.socket.close()
            self.socket = None
            print("Connexion fermé")
        except Exception as ex:
                        print(str(ex))





def main():

    s = ClientSocket()

    try:
        s.connect()
    except Exception as ex:
            print(str(ex))
    else:
        s.setCallbackMessageRecu(print)

        inp = None
        while(inp != "close"):
            inp = input("'ping' pour message serveur, 'close' pour fermer l'application : ")
            if(inp == "ping"):
                s.sendData(inp)
                time.sleep(1)


        s.close()



if __name__ == '__main__':
    main()