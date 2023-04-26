#this class is responsible for holding all the information for the game that we need (e.g. Did player1 go yet, what move did he, wat move did player2, are they connected to the server. It will also store things like keeping track of who won or lost), we're doing this in its own file because it is going to be accessed by both the client and the server
class Game:
    def __init__(self,id):
        self.p1Went = False #this stands for if player1 has made a move or not
        self.p2Went = False
        self.ready = False
        self.id = id #this stands for the current game id (each game we create will have its own id, to determine what clients are part of what game)
        self.moves = [None, None] #currently the moves are none
        self.wins = [0,0] #self.wins[0] stands for player1
        self.ties = 0

    def get_player_move(self, p): #this will get the player move that we ask for, 'p' will be either 0 or 1
        return self.moves[p]

    def player(self, player, move): #this is going to update our moves' list with that player's move
        self.moves[player] = move
        if player == 0: #based on the player we have to update if p1Went or p2Went
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self): #this is going to tell us if the two players are currently connected to the game, if that's the case it will allow us to load in, and that's how we can determine whether we should show "Waiting for player" or not on the screen
        return self.ready #that will tell us if we are ready, and that will be updated on the server side

    def bothWent(self): #this is going to tell us if both of our players are finished (they played each one move)
        return self.p1Went and self.p2Went

    def winner(self): #this is going to tell us who won the game, if we cal this method we're assuming that both players have gone, and we're going to check their moves against one another and see if they won, we have to check nine possible cases because there are three moves each player can do

        p1 = self.moves[0].upper()[0] #with this we're getting the first letter of the move, because the move is going to be stored as "rock", or "paper", or "scissors" (self.moves[0] is the player1's move)
        p2 = self.moves[1].upper()[0]

        winner = -1 #that's because there could be no winner, there could be a tie (égalité)
        if p1 == 'P' and p2 == 'R':
            winner = 0 #that means player1 wins
        elif p1 == 'P' and p2 == 'S':
            winner = 1 #that means player2 wins
        elif p1 == 'R' and p2 == 'P':
            winner = 1
        elif p1 == 'R' and p2 == 'S':
            winner = 0
        elif p1 == 'S' and p2 == 'P':
            winner = 0
        elif p1 == 'S' and p2 == 'R':
            winner = 1
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False