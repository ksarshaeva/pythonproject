import pygame
width = 1030
height = 580
floor = height-50
fps = 60

player_acc = 0.5
#player_gravity = 0.3
#player_acceleratio= 0.3


#colors
BLACK=(0,0,0)
WHITE = (255,255,255)
background = pygame.image.load("background.jpeg")

#set up assets(art and sound)
class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
        self.image = pygame.image.load('player_stand.png').convert()#how that sprite looks like
        self.image.set_colorkey(BLACK) #ignore background color of the image
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.rect.centerx = 145
        self.rect.bottom = floor
        self.speedy = 0
        self.speedx = 0
        
    def update(self):
        keystate=pygame.key.get_pressed() #gives a bool list of keys that are down(pressed)
        self.speedx = +2
        self.rect.x += self.speedx
        if keystate[pygame.K_w]:
            self.speedy = -5
        else:
            self.speedy += 1
        self.rect.y += self.speedy 

        #boundaries 
        if self.rect.top < 100: #doesn't go above the ceiling 
            self.rect.top = 100
        if self.rect.bottom > floor: #same for the floor
            self.rect.bottom = floor


#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Jetpack") #changing naming of the window
clock=pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player() #drawing the player
all_sprites.add(player)  #drawing the player

camera_x=0

running = True 
while running:

    if player.rect.x > width - width*0.75: #if it has reached 1/3 of the frame
        camera_x += -player.speedx
        
    clock.tick(fps)
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #update
    all_sprites.update() #telling the every sprite whatever their update rule is 

    #draw/render
    screen.fill(WHITE)
    screen.blit(background, (0,0))
    all_sprites.draw(screen)

    pygame.display.flip()
    
pygame.quit()

