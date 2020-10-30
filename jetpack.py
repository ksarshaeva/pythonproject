import pygame
import random
width = 1030
height = 580
floor = height - 50
fps=60

name = "spritesheet.png"
#colors
BLACK=(0,0,0)
WHITE = (255,255,255)

#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
"""
pygame.font.init()
welcome_font = pygame.font.SysFont('Comic Sans MS', 48)
instruction_font = pygame.font.SysFont('Comic Sans MS', 22)
"""
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
        self.alive = True 
        #for animation
        self.looks = Spritesheet(name)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.running_frame[0]#how that sprite looks like
        
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.rect.centerx = 140
        self.rect.bottom = floor
        self.speedy = 0
        self.speedx = 0

    def death(self):
        if not self.alive:
            self.speedy = 0
            self.speedx = 0


    def update(self):
        self.animate()
        keystate=pygame.key.get_pressed() #gives a bool list of keys that are down(pressed)
        if player.rect.right >= width / 3:
            self.speedx = 0
        else:
            self.speedx = +2.7
            self.rect.x += self.speedx
        if keystate[pygame.K_w]:
            self.speedy = -4  #flying up
            self.flying = True 
        elif not keystate[pygame.K_w]:
            self.speedy += 0.2    #gravity fall
        self.rect.y += self.speedy
            
        #boundaries 
        if self.rect.top < 100: #doesn't go above the ceiling 
            self.rect.top = 100
        if self.rect.bottom > height-50: #same for the floor
            self.rect.bottom = height-50

        if abs(self.rect.bottom - floor) < 10:
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
        self.rect.x = width+10 #making it appear from outside of our window
        self.rect.y = random.randrange(height-50,0,-10) #range for the location on the y axis 
        self.speed = random.randrange(3,8)
        
    def update(self):
        self.rect.x -= self.speed
        
class Shocker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.w = random.randrange(100, 500, 10)
        self.image = pygame.Surface((self.w, 35))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width, width + 100, 10)
        self.rect.y = random.randrange(height-75,90,-10)

    def update(self):
        for shocker in shockers:
            if shocker.rect.x + shocker.w < 1:
                shocker.kill()
        if not shockers:
            self.create_new()

    
    def create_new(self):
        for i in range(2):
            s = Shocker()
            all_sprites.add(s)
            shockers.add(s)

        

class Background():  #to move background with camera
      def __init__(self):
          self.background = pygame.image.load('fon.png').convert()
          self.background_rect = self.background.get_rect()

          self.bgY1 = 0
          self.bgX1 = 0

          self.bgY2 = 0
          self.bgX2 = self.background_rect.width
         
      def update(self):

        if player.rect.right >= width / 3:
            #moving shockers
            for shocker in shockers:
                shocker.rect.left -= 2.7
                
        #moving the background picture
            self.bgX1 -= 2.7
            self.bgX2 -= 2.7
        if self.bgX1 <= -self.background_rect.width:
            self.bgX1 = self.background_rect.width
        if self.bgX2 <= -self.background_rect.width:
            self.bgX2 = self.background_rect.width

      def render(self):
         screen.blit(self.background, (self.bgX1, self.bgY1))
         screen.blit(self.background, (self.bgX2, self.bgY2))


all_sprites = pygame.sprite.Group()
shockers = pygame.sprite.Group() #group to hold all shockers, to do collisions

s = Shocker().create_new()
        
mobs=pygame.sprite.Group()
player = Player() #drawing the player
background=Background()
all_sprites.add(player)#drawing the player
for i in range(2):
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)




#waiting = True 
running = True
while running:
   
    #keep loop running at the right speed
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            """
            waiting = False
        if event.type == pygame.K_SPACE:
            waiting = False
               """ 
    #process input 
    #приветствующее окно не убирается при нажатии пробела,  игра замораживается и "(He отвечает)"
        """
    while waiting:
        screen.fill(WHITE)
        game_name = welcome_font.render("Jetpack", False, BLACK)
        instruction1 = instruction_font.render("Press space to start", False, BLACK )
        screen.blit(game_name,(int(width/2), int(height/4)))
        screen.blit(instruction1,(int(width/2), int(height*3/4)))
        pygame.display.flip()
    """       
                
    #update
    background.update()
    
    #draw/render
    background.render()
    all_sprites.update() #telling the every sprite whatever their update rule is 
    all_sprites.draw(screen)
    
    pygame.display.flip()
    
pygame.quit()

