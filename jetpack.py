import pygame

width=1030
height=580
fps=10


#colors
BLACK=(0,0,0)
WHITE = (255,255,255)

#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Jetpack") #changing naming of the window
clock=pygame.time.Clock()

#set up assets(art and sound)

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
        self.image = pygame.image.load('player_stand.png').convert()#how that sprite looks like
        self.image.set_colorkey(BLACK) #ignore background color of the image
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.rect.centerx = 100
        self.rect.bottom = height-50
        self.speedy=0
        self.speedx=0
        
        

    def update(self):
        keystate=pygame.key.get_pressed() #gives a list of keys that are down(pressed)
        self.speedx+=1                     
        self.rect.x+=self.speedx    #moves to the right
        if keystate[pygame.K_SPACE]:
            self.speedy=-5
            self.rect.y +=self.speedy #flies if we press and hold space button
            if self.rect.y<0: 
                self.rect.y=0
        elif not keystate[pygame.K_SPACE]:
            while self.rect.bottom!=height-50:
                self.speedy=+5
                self.rect.y +=self.speedy
                


#Load all game graphics
background = pygame.image.load("fon.png").convert()
background_rect = background.get_rect()


all_sprites = pygame.sprite.Group()
player = Player() #drawing the player
all_sprites.add(player)  #drawing the player


running = True 
while running:
    #keep loop running at the right speed
    clock.tick(fps)
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
                
    #update
    all_sprites.update() #telling the every sprite whatever their update rule is 

    #draw/render
    screen.fill(WHITE)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    
    pygame.display.flip()
pygame.quit()

