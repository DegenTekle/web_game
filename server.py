import socket #we use these libraries (socket and _thread) to handle connection to our server
from _thread import * #it means that we're going to set up a socket, and it will allow for the connection to come in to our server on a certain port
import pickle
from game import Game

server = "192.168.115.148" #inserting IP address, the server address, type "ipconfig"  in terminal -> it's the IPv4
port = 5555 #it's a typical port that's open, it's going to look for certain connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setting up a socket, the parameters are just types of connection

try: #binding our server and our port to the socket (it's a test)
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) #listening for connections, it opens up the port so that we can start connecting to it and having multiple clients, if no parameters unlimited connections allowed
print("Waiting for a connection, Server Started") #at this point we are running the server and everything works

#Since we want to have unlimited connections at once, that means we're going to have unlimited games running at the same time, we're going to have a dictionary that contains a bunch of different games that will be accessed by their id
connected = set() #this is going to store the ip addresses of the connected clients
games = {} #this dictionary will store our games, it's going to have an id as a key, and a game object as a value
idCount = 0 #this keeps track of our current id, so we don't overwrite games and say that two games have the same id


def threaded_client(conn, p, gameId): #conn is an object that represents what's connected, this function will run in the background, we don't have to wait for it to finish before we can accept another connection, 'p' is the current player (0 or 1), 'gameId' stands for which game in 'games' dictionary are we playing
    global idCount #this is because if someone leaves our game or disconnects, we're going to need to subtract from that, so we can keep track of accordingly how many people are connected and how many games are running
    conn.send(str.encode(str(p))) #when someone connects to our server, we are going to send them what players are there

    reply = ""
    while True: #the way of sending string data from our client to our server is that we're going to send one of three options (get (when we want to get the name from the server, we're going to send that every frame), reset (when the game has finished, and we want to reset the game, this is going to be sent from the client's side), or a move -> "rock", "paper", or "scissors" (when the client makes a move, if it is allowed which will be checked on the client's side, we'll send that move to server which will update the game accordingly, and then it will send back the game to the client))
        try:
            data = conn.recv(4096).decode() #here we're going to constatly receive string data from the client, we write 4096 in case we're receiving too much information that is more than 2048 bits (we can go higher like 4096*2.. if we have any error)

            if gameId in games: #every time we run the while loop we're going to check if the game still exists, to see if the gameId which is the key TO access the game, because if one of our clients disconnect from the game we are going to delete that game
                game = games[gameId]

                if not data:
                    break
                else: #this happens if we receive data, we're going to check if we got a get, a reset or a move
                    if data == "reset": #that means it's a reset
                        game.resetWent()
                    elif data != "get": #that means it's a move
                        game.play(p, data) #we're going to send that move to update the game, p is the current player number, and the move is data

                    conn.sendall(pickle.dumps(game)) #this is going to package up our game into a sendable form, we're going to send it to our client, which will receive it, unpickle it, and then use it
            else:
                break
        except: #this prevents the server from stop running (in case there's something wrong with the "conn.recv(4096).decode()")
            break

    #if we break out of this while loop we need to close the game and delete it
    print("Lost connection")
    try: #we put try because f both players try to disconnect at the same time one player will delete the game before the other, so if the second try to delete a key that doesn't exist, we're going to run an issue
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True: #this while loop will continuously look for connections, this is where we're going to create new games based on new people joining
    conn, addr = s.accept() #this will allow any incoming connection and store it with its address, once a connection is accepted everything below runs
    print("Connected to:", addr) #this shows us what IP address is connecting

    idCount += 1 #this helps keeping track of how many people are connected to the server at once
    p = 0 #this stands for the current player
    gameId = (idCount - 1)//2 #with this, for every two people that connect to the server we're going to increment gameId by one, gameId will keep track of what id our game is going to be
    if idCount % 2 == 1: #this happens when we connect and the number of connections is odd, then we're going to need to create a new game, this helps to chose for the server who is going to be player1 and player2
        games[gameId] = Game(gameId) #with this, we say that "gameId" which is a key in our dictionary is now equals to the new game "Game(gameId)"
        print("Creating a new game...") #so that in our server we get some sort of output
    else: #this happens when we connect and we don't need to create a new game because the number of connections are even
        games[gameId].ready = True #this means that the second player is connected so now we can say that the game is ready to start playing, we are storing all the games on the server side
        p = 1 #we're going to assign that to the last player


    start_new_thread(threaded_client, (conn, p, gameId)) #here we are start a new thread, and we wait for another connection, we're going to send to the clients what player they are (0 or 1)
    #the server's script always have to be running, whenever we're trying to connect we have to first have run the server's script, and then we can run multiple clients scripts