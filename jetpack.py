import pygame
import random
from os import path

images_path = path.join(path.dirname(__file__), 'images')

width = 1030
height = 580
fps = 80
points = 0

#colors
BLACK=(0,0,0)
WHITE = (255,255,255)

#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Jetpack") #changing naming of the window
clock=pygame.time.Clock()

def draw_text(where, text, size, x, y):
    font = pygame.font.SysFont("Comis Sans MS", size)
    put = font.render(text, True, WHITE) #True - "anti-alias" - smoother letters(pixels)
    text_rect = put.get_rect()
    text_rect.center = (x, y)
    screen.blit(put, text_rect)
    
#set up assets(art and sound)
pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


shocker_animation = "lightning.png"
player_animation = "spritesheet.png"
mob_animation = "rocket_sprite.png"
#jetpack_sound = pygame.mixer.Sound(".wav")
#rocket_sound = pygame.mixer.Sound("missile.wav")
shocker_sound = pygame.mixer.Sound("shocker.wav")
get_coin_sound = pygame.mixer.Sound("coin.wav")
zapped_sound = pygame.mixer.Sound("zapped.wav")

class Spritesheet:
    def __init__(self,name, new_w, new_h):
        self.spritesheet = pygame.image.load(name).convert()
        self.new_w = new_w
        self.new_h = new_h

    def get_image(self,x,y,w,h):  #opens the spritesheet that we need to use
        image = pygame.Surface((w,h))
        image.blit(self.spritesheet, (0,0),(x,y,w,h))
        image = pygame.transform.scale(image,(self.new_w, self.new_h))
        return image
    
class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#built in function,without which sprite will not work
        self.flying = False
        self.alive = True 

        #for animation
        self.looks = Spritesheet(player_animation, 65, 110)
        self.current_frame = 0
        self.die_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.running_frame[0]#how that sprite looks like initially without animation
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.radius= int(self.rect.width/2)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centerx = 140
        self.rect.bottom = height-50
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
            self.speedy += 0.3    #gravity fall
        self.rect.y += self.speedy      

        #boundaries 
        if self.rect.top < 50: #doesn't go above the ceiling 
            self.rect.top = 50
        if self.rect.bottom > height-50: #same for the floor
            self.rect.bottom = height-50

        if abs(self.rect.bottom - (height -50)) < 10:
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

        self.run_die_frames = []
        for i in range(5):
            sprite = f'run_die{i}.png'
            image = pygame.image.load(path.join(images_path,sprite)).convert()
            size = image.get_size()
            image = pygame.transform.scale(image,(int(size[0]/5.62),int(size[1]/5.01)))
            image.set_colorkey(BLACK)
            self.run_die_frames.append(image)

        self.fly_die_frames = []
        for i in range(5):
            sprite = f'fly_die{i}.png'
            image = pygame.image.load(path.join(images_path,sprite)).convert()
            size = image.get_size()
            image = pygame.transform.scale(image,(int(size[0]/5.62),int(size[1]/5.01)))
            image.set_colorkey(BLACK)
            self.fly_die_frames.append(image)

            
    def animate(self):
        now = pygame.time.get_ticks()
        if self.alive:
            if not self.flying:
                if now - self.last_update > 60:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.running_frame)
                    self.image = self.running_frame[self.current_frame]
            else:
                if now  - self.last_update > 60:
                    self.last_update = now
                    self.current_frame = (self.current_frame +1) % len(self.flying_frame)
                    self.image = self.flying_frame[self.current_frame]
        else:#collided with an enemy
            if self.flying:
                while self.die_frame != 4:
                    if now - self.last_update > 60:
                        self.last_update = now
                        self.image = self.fly_die_frames[self.die_frame]
                    self.die_frame += 1
            else:
                while self.die_frame != 4:
                    if now - self.last_update > 60:
                        self.last_update = now
                        self.image = self.run_die_frames[self.die_frame]
                    self.die_frame += 1
                        
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('coin.png').convert()
        self.image = pygame.transform.scale(self.image,(40, 40))
        self.last_update = 0
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width+50,width,-5)
        self.rect.y = random.randrange(100,450)

    def update(self):
        if self.rect.x<0:
            self.rect.x = random.randrange(width+50,width,-5)
            self.rect.y = random.randrange(100,450)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.t=0
        self.looks = Spritesheet(mob_animation,100,62)
        self.current_frame = 0
        self.explode = False 
        self.last_update = 0 #keeps track when the last sprite change happened
        self.load_images()
        self.image = self.flying_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width*0.7/2)#for hits

        self.rect.x = width+20
        self.rect.y = random.randrange(height-150,70,-10)
        self.speedx = random.randrange(5,10)

    def load_images(self):
        self.flying_frames = [self.looks.get_image(155,20,153,82),
                                self.looks.get_image(155,103,153,82),
                                self.looks.get_image(155,192,153,78),
                                self.looks.get_image(155,294,153,82)]
        for frame in self.flying_frames:
            frame.set_colorkey(BLACK)     

    def update(self):
        self.animate()
        self.rect.x -= self.speedx
        now = pygame.time.get_ticks()
        if (self.rect.left<0) and (now-self.t>random.choice([20000,35000,40000,30000,50000])):
            self.t = now
            self.rect.x = width+20
            self.rect.y = random.randrange(height-50,0,-10)
            self.speedx = random.randrange(5,10)

            
    def animate(self):
        now = pygame.time.get_ticks()
        if now-self.last_update>150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.flying_frames)
            self.image = self.flying_frames[self.current_frame]

class Shocker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.w = random.randrange(200, 320, 15)
        self.image = pygame.Surface((self.w, 35)) #assign width and height
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width + 30, width + 80, 10)
        self.rect.y = random.randrange(100, 200, 20)
        self.t = 0

        #for animation
        self.looks = Spritesheet(shocker_animation, self.w, 35)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened
        self.load_images()
        self.image = self.shocker_frame[0]
        
    def update(self):
        self.animate()
        now = pygame.time.get_ticks()
        if (self.rect.left < 0) and (now-self.t > random.choice([20000,15000,40000,30000])):
            self.t = now
            for shocker in shockers:
                if shocker.rect.x + shocker.w < 1: #kill the sprite if it moved beyond our screen 
                    shocker.kill()

                if not shockers: 
                    self.create_new()
                

    def create_new(self):
        for i in range(2):
            s = Shocker()
            if i == 0:
                self.compare = s.rect.y
            if i == 1:
                s.rect.y = self.compare + 250
            all_sprites.add(s)
            shockers.add(s)
            
    def load_images(self):
        self.shocker_frame = [self.looks.get_image(0,19,513,95),
                              self.looks.get_image(0,147,513,95),
                              self.looks.get_image(0,247,513,95),
                              self.looks.get_image(0,403,513,95),
                              self.looks.get_image(0,531,513,95),
                              self.looks.get_image(0,659,513,95),
                              self.looks.get_image(0,787,513,95),
                              self.looks.get_image(0,915,513,95)]
        for frame in self.shocker_frame:
            frame.set_colorkey(BLACK)#ignore black background

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.shocker_frame)
            self.image = self.shocker_frame[self.current_frame]

class Explosion(pygame.sprite.Sprite):
    def __init__(self,coordinate ):
        pygame.sprite.Sprite.__init__(self)
        self.explode_frames = []
        for i in range(9):
            sprite = f'exp{i}.png'
            image = pygame.image.load(path.join(images_path,sprite)).convert()
            image = pygame.transform.scale(image,(90,90))
            image.set_colorkey(BLACK)
            self.explode_frames.append(image)


        self.image = self.explode_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = coordinate
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.frame +=1
            if self.frame == len(self.explode_frames):
                self.kill()
            else:
                coordinate = self.rect.center 
                self.image = self.explode_frames[self.frame]
                self.rect.center = coordinate

class Background():  #to move background with camera
      def __init__(self):
          self.background = pygame.image.load('fon.png').convert()#convert the size of the image to screen size
          self.background_rect = self.background.get_rect()

          self.bgY1 = 0
          self.bgX1 = 0
          self.bgY2 = 0
          self.bgX2 = self.background_rect.width
         
      def update(self):
        self.move = 2.7
        if player.rect.right >= width / 3:
            #moving shockers
            for shocker in shockers:
                shocker.rect.right -= self.move
            for c in coins:
                c.rect.right -= self.move 
            
        
                
        #moving the background picture
            self.bgX1 -= self.move 
            self.bgX2 -= self.move 
        if self.bgX1 <= -self.background_rect.width:
            self.bgX1 = self.background_rect.width
        if self.bgX2 <= -self.background_rect.width:
            self.bgX2 = self.background_rect.width

      def render(self):
         screen.blit(self.background, (self.bgX1, self.bgY1))
         screen.blit(self.background, (self.bgX2, self.bgY2))

def starting_screen():
    background = pygame.image.load('fon.png').convert()
    screen.blit(background, (0,0))

    draw_text(screen, "Jetpack!", 64, width / 2, height / 4)
    draw_text(screen, "press W to fly up", 22, width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width / 2, height *3/4)
    draw_text(screen, str(points), 22, width/2, 20)
    pygame.display.flip()
    waiting = True 
    while waiting:
        pygame.init()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
               waiting = False
 
def game_over_screen():
    background = pygame.image.load('fon.png').convert()
    screen.blit(background, (0,0))
    draw_text(screen, "GAME OVER", 48, width / 2, height / 4)
    draw_text(screen,"Score: "+ str(score),30,width/2,height/2)
    draw_text(screen, "Press a key to play again", 18, width / 2, height*3/4)
    pygame.display.flip()
    waiting = True 
    while waiting:
        pygame.init()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
      

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
coins = pygame.sprite.Group()
shockers = pygame.sprite.Group()
player = Player() #drawing the player
coins= pygame.sprite.Group()
background=Background()
all_sprites.add(player)#drawing the player
shockers = pygame.sprite.Group() 
s = Shocker().create_new()

  
for i in range(2):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
for i in range(5):
    c=Coins()
    all_sprites.add(c)
    coins.add(c)

score=0
waiting = False
game_over = False
running = True 
pause = False
starting_screen()
while running:
    if game_over:
        game_over_screen()
        game_over = False
        score=0
        all_sprites = pygame.sprite.Group()
        shockers = pygame.sprite.Group() #group to hold all shockers, to do collisions
        s = Shocker().create_new()
        coins = pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        player = Player() #drawing the player
        coins= pygame.sprite.Group()
        background=Background()
        all_sprites.add(player)#drawing the player
        for i in range(2):
            m=Mob()
            all_sprites.add(m)
            mobs.add(m)
        for i in range(5):
            c=Coins()
            all_sprites.add(c)
            coins.add(c)
    #keep loop running at the right speed
    clock.tick(fps) 
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #check if player hit any of the sprites
    hits = pygame.sprite.spritecollide(player, shockers, False,pygame.sprite.collide_rect_ratio(0.7))#makes the rect smaller so that collisions will be more accurate
    if hits:
        player.alive = False
        game_over = True
        
    hits=pygame.sprite.spritecollide(player,mobs,True,pygame.sprite.collide_circle) #True makes the enemy disappear
    for hit in hits:
        explode = Explosion(hit.rect.center)
        all_sprites.add(explode)
        player.alive = False
        game_over=True

    hits=pygame.sprite.spritecollide(player,coins,True,pygame.sprite.collide_rect_ratio(0.7))
    for hit in hits:
        get_coin_sound.play()
        score+=1
        c = Coins()
        all_sprites.add(c)
        coins.add(c)

    #update
    background.update()
    
    #draw/render
    background.render()
    all_sprites.update() #telling the every sprite whatever their update rule is 
    all_sprites.draw(screen)
    draw_text(screen,'Score: '+str(score),30,width/2,50)
    pygame.display.flip()
    
pygame.quit()






            


