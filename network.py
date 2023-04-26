import socket
import pickle


class Network: #creating a class that will be responsible to connecting to our server
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.115.148" #this variable must be the same as the one in the server's script
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect() #when we connect to our server we want to return to each of the clients the starting position of their character (it will differ either it's player1 or player2)

    def getP(self):
        return self.p

    def connect(self):
        try: #we do this just in case it's not working
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() #once we are connected we'll receive some information immediately back (our player's number), we are going to be receiving an object, we're going to decode a string from it
        except:
            pass

    def send(self, data): #this method is useful to send data to the server
        try:
            self.client.send(str.encode(data)) #we're going to send a string data to the server, and we're going to receive back object data
            return pickle.loads(self.client.recv(2048*2)) #we're going to load an object get a reply from the server
        except socket.error as e:
            print(e) #allows us to have look at the error we have if it happens

