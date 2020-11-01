import pygame
import random
width = 1030
height = 580
fps = 80

shocker_animation = "lightning.png"
player_animation = "spritesheet.png"
coin_animation = "coin.png"
mob_animation = "rocket_sprite.png"

#colors
BLACK=(0,0,0)
WHITE = (255,255,255)

#initializing pygame and creating a window 
pygame.init()
pygame.mixer.init() #sounds
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Jetpack") #changing naming of the window
clock=pygame.time.Clock()
"""
def choose_spawn(): #чтобы игра не была скучной, и шокеры иногда появлялись иногда нет, и то же самое для монеток
    answer = random.choice(True, False)
    print(answer)
    return answer"""
def draw_text(where, text, size, x, y):
    font = pygame.font.SysFont("Comis Sans MS", size)
    put = font.render(text, True, BLACK)
    text_rect = put.get_rect()
    text_rect.center = (x, y)
    screen.blit(put, text_rect)
#set up assets(art and sound)
class Spritesheet:
    def __init__(self,name, new_w, new_h):
        self.spritesheet = pygame.image.load(name).convert()
        self.new_w=new_w
        self.new_h=new_h

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
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.running_frame[0]#how that sprite looks like initially without animation
        self.rect = self.image.get_rect()#rectangle that incloses the sprite
        self.radius= int(self.rect.width/2)
        #pygame.draw.circle(self.image,WHITE,self.rect.center,self.radius)
        self.rect.centerx = 140
        self.rect.bottom = height-50
        self.speedy = 0
        self.speedx = 0

    def death(self): #it's not uset yet
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
            self.speedy = -3  #flying up
            self.flying = True 
        elif not keystate[pygame.K_w]:
            self.speedy += 0.1    #gravity fall
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
            
    def animate(self):
        now = pygame.time.get_ticks()
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
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.looks = Spritesheet(mob_animation,100,62)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.flying_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius= int(self.rect.width*0.7/2)
        #pygame.draw.circle(self.image,WHITE,self.rect.center,self.radius)
        self.rect.x=width+20
        self.rect.y=random.randrange(height-70,0,-10)
        self.speedx=random.randrange(5,10)

    def load_images(self):
        self.flying_frames = [self.looks.get_image(155,20,153,82),
                                self.looks.get_image(155,103,153,82),
                                self.looks.get_image(155,192,153,78),
                                self.looks.get_image(155,294,153,82)]
        for frame in self.flying_frames:
            frame.set_colorkey(BLACK)

        
    def update(self):
        self.animate()
        self.rect.x-=self.speedx
        if self.rect.left<0:
            self.rect.x=width+20
            self.rect.y=random.randrange(height-50,0,-10)
            self.speedx=random.randrange(5,10)

            
    def animate(self):
        now=pygame.time.get_ticks()
        if now-self.last_update>150:
            self.last_update=now
            self.current_frame = (self.current_frame + 1)% len(self.flying_frames)
            self.image=self.flying_frames[self.current_frame]
        
#rocket fly1=(155,20,153,82)
#rocket fly2=(155,103,153,82)
#rocket fly3=(155,192,153,78)
#rocket fly4=(155,294,153,82)


class Shocker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.w = random.randrange(200, 320, 15)
        self.image = pygame.Surface((self.w, 35)) #assign width and height
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width + 30, width + 80, 10)
        self.rect.y = random.randrange(100, 200, 20)

        #for animation
        self.looks = Spritesheet(shocker_animation, self.w, 35)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.shocker_frame[0]

    def update(self):
        self.animate()
        for shocker in shockers:
            if shocker.rect.x + shocker.w < 1: #kill the sprite if it moved beyond our screen 
                shocker.kill()

        if not shockers: #and random.choice([True, False])
            self.create_new()

    def create_new(self):
        for i in range(2):
            s = Shocker()
            if i == 0:
                self.compare = s.rect.y
            if i == 1:
                """ work on this 
                if choose_spawn():#create coins in between the shockers

                """
                s.rect.y = self.compare + 250
            all_sprites.add(s)
            shockers.add(s)
            """ need to work on this 
        if choose_spawn():#create coins after shockers to fill the empty space
            c = Coins((self.compare + 35) + 25, (self.compare + 250) - 25)
            """

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
        
"""
class Coins(pygame.sprite.Sprite):
    def __init__(self, upperlimit, lowerlimit):
        self.indent_ceiling = 90 #отступ сверху 
        self.indent_between = 10 #отступ между каждым рядом и строкой 
        self.sides = 30 #width and height 
        if upperlimit != 0 and lowerlimit != 0: #if we spawn then in between shockers 
            self.rows = random.randrange()
            self.columns = random.randrange()
        else:
            self.rows = random.randrange(1, 6, 1)
            self.columns = random.randrange(1, 11, 2)

        self.image = pygame.Surface((self.sides, self.sides)) #assign width and height
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        #self.rect.x = random.randrange(width + 30, width + 80, 10) #i'm not sure how to this 
        self.rect.y = random.randrange(self.indent_ceiling, self.indent_ceiling + 60, 10)

        #for animation
        self.looks = Spritesheet(coin_animation, self.sides, self.sides)
        self.current_frame = 0
        self.last_update = 0 #keeps track when the last sprite change happened 
        self.load_images()
        self.image = self.coin_frame[0] #how that sprite looks like initially without animation

    def create_new():
        c = Coins(, ) #из-за того что теперь там может быть лимиты, здесь это идет цикл без конца
            
    def load_images(self):
        self.coin_frame = [ self.looks.get_image(0,0,84,84),
                            self.looks.get_image(84,0,84,84),
                            self.looks.get_image(168,0,84,84),
                            self.looks.get_image(252,0,84,84),
                            self.looks.get_image(336,0,84,84),
                            self.looks.get_image(420,0,84,84)]
        for frame in self.coin_frame:
            frame.set_colorkey(BLACK) #ignore black background

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.coin_frame)
            self.image = self.coin_frame[self.current_frame]
"""

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
                shocker.rect.right -= 2.7
                
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

def show_go_screen():
    screen.fill(WHITE)
    draw_text(screen, "Jetpack!", 64, width / 2, height / 4)
    draw_text(screen, "press W to fly up", 22, width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width / 2, height *3/4)
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
        
waiting = False
game_over = True

all_sprites = pygame.sprite.Group()
mobs=pygame.sprite.Group()
player = Player() #drawing the player
background=Background()
mob_img=pygame.image.load('rocket.png').convert()
all_sprites.add(player)#drawing the player

for i in range(2):
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)



running = True 
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        shockers = pygame.sprite.Group() #group to hold all shockers, to do collisions
        coins = pygame.sprite.Group()
        s = Shocker().create_new()
        mobs=pygame.sprite.Group()
        player = Player() #drawing the player
        background=Background()
        all_sprites.add(player)#drawing the player
        for i in range(2):
            m=Mob()
            all_sprites.add(m)
            mobs.add(m)
    #keep loop running at the right speed
    clock.tick(fps) 
    #process input 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    hits = pygame.sprite.spritecollide(player, shockers, False)
    if hits:
        game_over = True        
    #update
    background.update()
    
    #draw/render
    background.render()
    all_sprites.update() #telling the every sprite whatever their update rule is 
    #check to see if a mob hit the player
    hits=pygame.sprite.spritecollide(player,mobs,False,pygame.sprite.collide_circle)
    if hits:
        running=False
    all_sprites.draw(screen)
    
    pygame.display.flip()
    
pygame.quit()

