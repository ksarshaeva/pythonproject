import pygame

width=1030
height=630
fps=60

#colors
BLACK=(0,0,0)
WHITE = (255,255,255)

#set up assets(art and sound)

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
        self.image = pygame.image.load('player_stand.png').convert()#how that sprite looks like
        self.image.set_colorkey(BLACK) #ignore background color of the image
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.rect.centerx = 145
        self.rect.bottom = height-150
        
        

    def update(self):
        keystate=pygame.key.get_pressed() #gives a list of keys that are down(pressed)
        


#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Jetpack") #changing naming of the window
clock=pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player() #drawing the player
all_sprites.add(player)  #drawing the player

running = True 
while running:

    clock.tick(fps)
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #update
    all_sprites.update() #telling the every sprite whatever their update rule is 

    #draw/render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
pygame.quit()

