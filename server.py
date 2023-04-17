import socket #we use these librairies (socket and _thread) to handle connection to our server
from _thread import * #it means that we're going to set up a socket and it will allow for the connection to come in to our server on a certain port
import sys

server = "172.30.11.83" #inserting IP adress, the server adress, type "ip"c  in terminal -> it's the IPv4
port = 5555 #it's a typical port that's open, it's going to look for certain connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setting up a socket, the parameters are just types of connection

try: #binding our server and our port to the socket (it's a test)
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2) #listening for connections, it opens up the port so we can start connecting to it and having multiple clients, if no paramaters unlimited connections allowed
print("Waiting for a connection, Server Started") #at this point we are running the server and everything works

def threaded_client(conn): #conn is an object that represents what's connected, this function will run in the background, we don't have to wait for it to finish before we can accept another connection
    conn.send(str.encode("Connected")) #when we connect we should send some validation token or id back to our network object or back to our client
    reply = ""
    while True: #we want this to continually run while our client is still connected
        try:
            data = conn.recv(2048) #we want to receive some kind of data from our connection, the larger is the parameter the longer it's going to take to receive information
            reply = data.decode("utf-8") #we do this because whenever we're sending information over a client server system we have to incode the information

            if not data: #if we try to get some information from the client but aren't getting anything, we'll disconnect and break (instead of trying to get information from a client that's disconnected)
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply)) #to send information over the server we have to encode it (it's for security)
        except:
            break

    print("Lost connection")
    conn.close()

while True: #this while loop will continuously look for connections
    conn, addr = s.accept() #this will any incoming connection and store it as well as its adress
    print("Connected to: ", addr) #this shows us what IP adress is connecting

    start_new_thread(threaded_client, (conn, ))

#the server's script always have to be running, whenever we're trying to connect we have to first have run the server's script and then we can run multiple clients scripts