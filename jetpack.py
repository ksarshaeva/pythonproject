import pygame
import random
width = 1030
height = 580
fps=60

name = "spritesheet.png"
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
class Spritesheet:
    def __init__(self,name):
        self.spritesheet = pygame.image.load(name).convert()

    def get_image(self,x,y,w,h):  #opens the spritesheet that we need to use
        image = pygame.Surface((w,h))
        image.blit(self.spritesheet, (0,0),(x,y,w,h))
        image = pygame.transform.scale(image,(75,120))
        return image
    
class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
        self.flying = False
        self.looks = Spritesheet(name)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.running_frame[0]#how that sprite looks like
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.rect.centerx = 145
        self.rect.bottom = height-50
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.animate()
        keystate=pygame.key.get_pressed() #gives a bool list of keys that are down(pressed)
        self.speedx = +2
        self.rect.x += self.speedx
        if keystate[pygame.K_w]:
            self.speedy = -5  #flying up
            self.flying = True 
        elif not keystate[pygame.K_w]:
            self.speedy += 0.4    #gravity fall
        self.rect.y += self.speedy
            
        #boundaries 
        if self.rect.top < 100: #doesn't go above the ceiling 
            self.rect.top = 100
        if self.rect.bottom > height-50: #same for the floor
            self.rect.bottom = height-50
            self.flying = False
            
    def load_images(self):
        self.running_frame = [self.looks.get_image(198,0,365,552),
                              self.looks.get_image(889,0,365,552),
                              self.looks.get_image(1580,0,365,552),
                              self.looks.get_image(2273,0,365,552),
                              self.looks.get_image(2965,0,365,552),
                              self.looks.get_image(198,599,365,552),
                              self.looks.get_image(889,599,365,552),
                              self.looks.get_image(1580,599,365,552),
                              self.looks.get_image(2273,599,365,552),
                              self.looks.get_image(2965,599,365,552),
                              self.looks.get_image(198,1198,365,552),
                              self.looks.get_image(889,1198,365,552),
                              self.looks.get_image(1580,1198,365,552),
                              self.looks.get_image(2273,1198,365,552),
                              self.looks.get_image(2965,1198,365,552)]
        for frame in self.running_frame:
            frame.set_colorkey(BLACK)#ignore black background
            
        self.flying_frame = [self.looks.get_image(289,1814,317,552),
                             self.looks.get_image(981,1814,317,552),
                             self.looks.get_image(1673,1814,317,552), 
                             self.looks.get_image(2365,1814,317,552),
                             self.looks.get_image(3057,1814,317,552),
                             self.looks.get_image(289,2413,317,552),
                             self.looks.get_image(981,2413,317,552),
                             self.looks.get_image(1673,2413,317,552),
                             self.looks.get_image(2365,2413,317,552),
                             self.looks.get_image(3057,2413,317,552),
                             ]
        for frame in self.flying_frame:
            frame.set_colorkey(BLACK)
            
    def animate(self):
        now = pygame.time.get_ticks()
        if not self.flying:
            if now - self.last_update > 90:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.running_frame)
                self.image = self.running_frame[self.current_frame]
        else:
            if now  - self.last_update > 110:
                self.last_update = now
                self.current_frame = (self.current_frame +1) % len(self.flying_frame)
                self.image = self.flying_frame[self.current_frame]
        
    
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

          self.moving_speed = 5
         
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

