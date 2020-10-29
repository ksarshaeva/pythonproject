import pygame
width = 1030
height = 580
fps = 60

name = "spritesheet.png"
#colors
BLACK=(0,0,0)
WHITE = (255,255,255)
background = pygame.image.load("background.jpeg")

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
        self.flying = False
        self.looks = Spritesheet(name)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.running_frame[0]#how that sprite looks like
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
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

