import pygame

width = 500
height = 500
win = pygame.display.set_mode((width, height)) #creation of a window
pygame.display.set_caption("Client")

clientNumber = 0 #setting up a global variable
class Player(): #setting up a class for our character
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height) #this will make it faster when we're trying to draw our character
        self.vel = 3

    def draw(self, win): #with this function we'll draw our character
        pygame.draw.rect(win, self.color, self.rect) #that's all we need to do to draw the character

    def move(self): #this function checks for keyboard inputs to move the character
        keys= pygame.key.get_pressed() #dictionnary where each key has a value of 1 or 0, 1 if the "key" is being pressed 0 if not

        if keys[pygame.K_LEFT]: #(left arrow key)
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel #that's how it is pygame (to go down we have to add to it)

        self.rect = (self.x, self.y, self.width, self.height) #this allows us to update the rect every time we make a move

def redrawWindow(win, player):
    win.fill((255,255,255))
    player.draw(win)
    pygame.display.update()


def main(): #Here we create the game loop, and this is going to run continuously while the program's going
    run = True
    player1 = Player(50,50,100,100,(0,255,0)) #creating a player object

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.QUIT()

        player1.move() #this allows us to move the character based on what keys we're pressing
        redrawWindow(win,player1)

main() #with this we execute the code that we wrote