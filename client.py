#in this script we've got about 150 lines, this is mostly due to dealing with the drawing part, making the buttons working, and display the text (that's what it takes to make on online graphical game)
import pygame
from network import Network #we're going to import the network class because we're going to use it here
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height)) #creation of a window
pygame.display.set_caption("Client")


class Button: #this generates button, because we have three buttons it will make things easier
    def __init__(self, text, x, y, color): #we will say that the width and the height will be uniformed, and will make the three same buttons
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos): #this is going to define each button's area, thus help us to know if we clicked on a button or not
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height: #this is logic, we check if x and y coordinates are in the button (that's a pygame collision)
            return True
        else:
            return False


def redrawWindow(win, game, p): #with this function we draw on the screen
    win.fill((128,128,128))

    if not(game.connected()): #this happens if we have not yet the other player connected
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True) #the "True" here stands for "bold"
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else: #this happens if both players are connected
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255)) #we're going to start with "Your move" statement and "Opponent" because those two aren't going to change, they're going to stay the same no matter what
        win.blit(text, (80, 200)) #we're displaying the text at a static position on the screen

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200)) #here we change the text's 'x' value so that we draw it aside of "Your move"

        #here we want to draw the moves (we want to know what move is, but we don't want to show the other player what our move is, unless both of them are finished)
        move1 = game.get_player_move(0) #we start by getting the two players' move
        move2 = game.get_player_move(1)

        #now we're going to check if we should show these moves, should show "Waiting", or should show "Hidden"
        if game.bothWent(): #this happens when both players have played their turn
            text1 = font.render(move1, 1, (0,0,0)) #this is saying, if both of players have played their turn, we can show their move
            text2 = font.render(move2, 1, (0, 0, 0))

        else: #this happens if both players haven't finished playing their turn
            if game.p1Went and p == 0: #this happens if player1 has already played,not yet player2, and we're player1
                text1 = font.render(move1, 1, (0,0,0)) #we're going to display this underneath "Your move"
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0)) #we're going to display this underneath "Opponent"
            else: #this happens if player1 hasn't played his turn yet
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1: #this happens if player2 has already played,not yet player1, and we're player2
                text2 = font.render(move2, 1, (0,0,0)) #we're going to display this underneath "Your move"
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0)) #we're going to display this underneath "Opponent"
            else: #this happens if player2 hasn't played his turn yet
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        #the text2 is dedicated to the player2 and the text1 to the player1
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win) #we're displaying the buttons

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))] #we're defining the three buttons at the bottom of the screen "rock", "paper", and "scissors"
def main(): #below until the while loop it's the "start" part of the game which is executed only once
    run = True
    clock = pygame.time.Clock()
    n = Network() #this is when we initially connect to the server
    player = int(n.getP()) #it returns the data of who we're connected to (which is the player's number)
    print("You are player", player) #this indicates to us when we initially run if we are player 0 or 1, to see if everythig is working

    while run: #it's the loop that is the game, and this is going to run continuously while the program's going, it tells what will happen every frame
        clock.tick(60)
        #we're connecting and asking the server for information, every frame we're asking the server to send us the game
        try: #we do the "try thing" because if we send this and we don't get a response from the server, that means the game doesn't exist
            game = n.send("get")
        except: #if that happens we should exit out of this game, and we should try to reconnect, or start a new game with someone else
            run = False
            print("Couldn't get game")
            break #the main function will be the actual game running, once we exit this main function we're going to go to the main menu (which will allow us to choose who we want to play against, etc...)

        if game.bothWent(): #now (we're not waiting for anything) we're going to see which player won, and display that message accordingly on the screen
            redrawWindow(win, game, player) #by doing this we want to make sure if both players went, we're updating the window and on the window it will check if both players have gone, and it will draw the player's moves for us
            pygame.time.delay(500) #we're applying a little delay of 0.5 second so that we can see what both players did before immediately pop up the winning result
            try:
                game = n.send("reset") #we're doing ths because when both players went, and we need to tell the server to reset those players moves two allow both players to move on the next game
            except:
                run = False
                print("Couldn't get game")
                break

            #after we've sent that reset we want to display a message on the screen indicating whether player1 or player2 did
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2)) #we're putting the font in the middle of the screen (to blit means to display)
            pygame.display.update()
            pygame.time.delay(2000) #2000ms so it's equal to 2 seconds, and then we're going to play the game again after

        for event in pygame.event.get(): #that means if the players hit the little 'x' button on the corner it will quit the game
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN: #this happens if the player actually presses the button down
                pos = pygame.mouse.get_pos() #here we're getting the mouse's location

                #now for every single button, if the mouse's location is on it we're going to do something accordingly
                for btn in btns:
                    if btn.click(pos) and game.connected(): #the "btn.click(pos)" part tells us if the area we clicked on was an actual button area, the "game.connected()" part is to make sure that it's not going to let us press "Rock", "Paper", or "Scissors" unless the both players are on (avoid issue where one player can make a move before the other connects)
                        if player == 0: #we're checking where our current player is, this is going to determine how we send a move
                            if not game.p1Went: #that means if player1 has not played his turn yet
                                n.send(btn.text) #to make a move we need to send to the server our move, we're just going to send the text of the button
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main() #with this we execute the code that we wrote

while True:
    menu_screen()
