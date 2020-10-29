import pygame
import random
width=1030
height=580
fps=25


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
        self.speedx=1                     
        self.rect.x+=self.speedx    #moves to the right
        if keystate[pygame.K_SPACE]:
            self.speedy=-5
            self.rect.y+=self.speedy#flies if we press and hold space button
            if self.rect.top<100: 
                self.rect.top=100
        elif not keystate[pygame.K_SPACE]:
            self.speedy+=0.7
        self.rect.y +=self.speedy
        if self.rect.bottom > height-50:
            self.rect.bottom=height-50


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('rocket.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x=random.randrange(width+10)
        self.rect.y=random.randrange(height-50,0,-10)
        self.speedx=random.randrange(1,8)
    def update(self):
        self.rect.x-=self.speedx
        
class Background():  #to move background with camera
      def __init__(self):
            self.background = pygame.image.load('fon.png').convert()
            self.background_rect = self.background.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.background_rect.width
 
            self.moving_speed =5
         
      def update(self):
        #self.moving_speed+=1
        self.bgX1 -= self.moving_speed
        self.bgX2 -= self.moving_speed
        if self.bgX1 <= -self.background_rect.width:
            self.bgX1 = self.background_rect.width
        if self.bgX2 <= -self.background_rect.width:
            self.bgX2 = self.background_rect.width
             
      def render(self):
         screen.blit(self.background, (self.bgX1, self.bgY1))
         screen.blit(self.background, (self.bgX2, self.bgY2))


all_sprites = pygame.sprite.Group()
mobs=pygame.sprite.Group()
player = Player() #drawing the player
background=Background()
all_sprites.add(player)#drawing the player
for i in range(2):
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)



running = True 
while running:
    

        
    #keep loop running at the right speed
    clock.tick(fps)
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
           
                
    #update
    background.update()
    #draw/render
    background.render()
    all_sprites.update() #telling the every sprite whatever their update rule is 
    all_sprites.draw(screen)
    
    pygame.display.flip()
pygame.quit()

