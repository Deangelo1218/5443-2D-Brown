import pygame
import os
from pygame import mixer
from pygame.locals import *


pygame.init()
mixer.init()

WIDTH =  800
HEIGHT = 800
#HEIGHT = int(WIDTH * 0.8)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Multiplayer')

clock = pygame.time.Clock()
FPS = 60

#Game variable

gravity = 0.65
# pygame.mixer.music.load("sound/music.wav")
# pygame.mixer.Sound('sound/music.wav')
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)

shooting  = pygame.mixer.Sound('sound/pew.wav')
shooting.set_volume(0.5)

#Player action variables

move_left = False
move_right = False
shoot = False

move_left2 = False
move_right2 = False
shoot2 = False

#load images

#bullet
bullet_img = pygame.image.load('img/bullet/bullet.png').convert_alpha()
proj_img = pygame.image.load('img/project/projectile.png').convert_alpha()

BG = (144,201,120)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)


tile_size = 50

#sun_img = pygame.image.load('img/sun.png').convert_alpha()
bg_img = pygame.image.load('img/map.jpg').convert_alpha()


class Champion(pygame.sprite.Sprite):
    def __init__(self, char_type, x , y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.shoot_cooldown = 0
        self.speed = speed
        self.vel_y = 0

        self.health = 100
        self.max_health = self.health

        self.direction = 1
        self.jump = False
        self.in_air = True
        self.crouch = False

        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all images for players

        animation_types = ['Idle', 'Walk', 'Jump', 'Death', 'Crouch']
        temp_list = []

        for animation in animation_types:
            #reset temp list
            temp_list = []
            #count number files
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img =pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
      

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
    

    def update(self):
        self.update_animation()
        self.check_alive()
        self.check_crouch()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -=1

             

    def move(self, moving_left, moving_right):
        #reset movement variable
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
          
        
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True


        #apply gravity
        self.vel_y += gravity 
        if self.vel_y > 10:
            self.vel_y 
        dy += self.vel_y
    

        for tile in feild.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #below ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False


        


        self.rect.x += dx
        self.rect.y += dy

        if self.rect.x > WIDTH:
            self.rect.x =0
            self.rect.y = HEIGHT - 50
        
        if self.rect.x < 0:
            self.rect.x = WIDTH
            self.rect.y = HEIGHT -50
        

    
        


            

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery + 11, self.direction)
            bullet_group.add(bullet)
            shooting.play()


    def update_animation(self):
        #update animation
        cooldown = 100

        #update image depending on currect frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update

        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        #if animation run out reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is different to previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
    
    def check_crouch(self):
        if self.crouch:
            self.update_action(4)

    
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

        #check collision with champs
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -=20
                self.kill()



        if pygame.sprite.spritecollide(player2, bullet_group, False):
            if player2.alive:
                player2.health -=20
                self.kill()



class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = proj_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction



class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x =x
        self.y = y
        self.health = health
        self.max_health = max_health

    
    def draw(self, health):
        self.health = health
        
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))





summoner_rift = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0], 
[0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0,  0, 8, 0], 
[0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0,  2, 2, 2], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0,  0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2,  0, 0, 0], 
[0, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0,  0, 0, 0], 
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0,  0, 0, 0], 
[0, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0,  0, 0, 0], 
[0, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0,  0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2,  2, 2, 2], 
[0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0,  1, 1, 1], 
[0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1], 
[0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1], 
[2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,  1, 1, 1]
]



class Terrain():
    def __init__(self, data):
        self.tile_list = []
        

    
        dirt = pygame.image.load('img/dirt.png')
        grass = pygame.image.load('img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    #player = Champion('Player', row_count * tile_size, col_count * tile_size, 1.65, 5)
                if tile == 2:
                    img = pygame.transform.scale(grass,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
        
    
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])



feild = Terrain(summoner_rift)


#create sprite groups

bullet_group  = pygame.sprite.Group()
      

player = Champion('Player',40, 400, 3, 5) 
player2 = Champion('player2',600, 400, 3, 5) 
hp = HealthBar(40, 20, player.health, player.health)
hp_p2 = HealthBar(600, 20, player2.health, player2.health)





run = True

while run:

    
    clock.tick(FPS)

    #draw_bg()
    screen.blit(bg_img, (0,0))
    #screen.blit(sun_img, (100,100))

    hp.draw(player.health)
    hp_p2.draw(player2.health)
    feild.draw()

    #draw_grid()

    player.update()
    player.draw()

    player2.update()
    player2.draw()

   
    #update player action

    bullet_group.update()
    bullet_group.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2) #2: jump
        
       

        elif move_left or move_right:
            player.update_action(1) #1: walk



        else:
            player.update_action(0) #0:idle
           
        player.move(move_left, move_right)
        
    
    if player2.alive:
        if shoot2:
            player2.shoot()
        
        if player2.in_air:
            player2.update_action(2) #2: jump

        elif move_left2 or move_right2:
            player2.update_action(1) #1: walk


        else:
            
            player2.update_action(0) #0:idle
        player2.move(move_left2, move_right2)

 
   
    
    

    for event in pygame.event.get():
        #quit the game
        if event.type == pygame.QUIT:
            run = False
        
        #Checking for keys being held down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True

            if event.key == pygame.K_LEFT:
                move_left2 = True
            if event.key == pygame.K_RIGHT:
                move_right2 = True
            if event.key == pygame.K_UP and player2.alive:
                player2.jump = True
            if event.key == pygame.K_1:
                shoot2 = True

            if event.key == pygame.K_RETURN:
                player = Champion('Player',40, 400, 3, 5) 
                player2 = Champion('player2',600, 400, 3, 5) 
                hp = HealthBar(40, 20, player.health, player.health)
                hp_p2 = HealthBar(600, 20, player2.health, player2.health)
    
                

            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_2:
                prod = True


        #Releasing the key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_LEFT:
                move_left2 = False
            if event.key == pygame.K_RIGHT:
                move_right2 = False
            if event.key == pygame.K_UP and player2.alive:
                player2.jump = False
            if event.key == pygame.K_1:
                shoot2 = False
            if event.key == pygame.K_2:
                prod = False
        
            

    pygame.display.update()       
               
pygame.quit()
