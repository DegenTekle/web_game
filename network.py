import socket


class Network: #creating a class that will be responsible to connecting to our server
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.30.11.83" #this variable must be the same as the one in the server's script
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id) #it should say "Connected" (a message decoded which incoded and sent by the server)

    def connect(self):
        try: #we do this just in case it's not working
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() #once we are connected we'll receive some information immediately back
        except:
            pass

    def send(self, data): #this method is useful to save time (send data to the server)
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode() #we're going to get a reply from the server
        except socket.error as e:
            print(e) #allows us to have look at the error we have if it happens


n = Network()
print(n.send("hello"))
print(n.send("working"))