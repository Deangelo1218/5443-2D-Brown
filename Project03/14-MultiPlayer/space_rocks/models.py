from pygame.math import Vector2
from pygame import transform
from pygame import time
from PIL import Image
from utils import get_random_velocity, load_sound, load_sprite, load_sprite_rotated, wrap_position, distance
import math
import os
import pygame
import random
import json

UP = Vector2(0, -1)


"""
 ██████╗  █████╗  ██████╗██╗  ██╗ ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗██████╗ 
 ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔════╝ ██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔══██╗
 ██████╔╝███████║██║     █████╔╝ ██║  ███╗██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║  ██║
 ██╔══██╗██╔══██║██║     ██╔═██╗ ██║   ██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║  ██║
 ██████╔╝██║  ██║╚██████╗██║  ██╗╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║██████╔╝
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ 
                                                                                      
 ██╗███╗   ███╗ █████╗  ██████╗ ███████╗██████╗ ██╗   ██╗                             
 ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔══██╗╚██╗ ██╔╝                             
 ██║██╔████╔██║███████║██║  ███╗█████╗  ██████╔╝ ╚████╔╝                              
 ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝                               
 ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗██║  ██║   ██║                                
 ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝                                                                                                          
"""
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, size):

        pygame.sprite.Sprite.__init__(self)
        self.width, self.height = self.getImgWidthHeight(image_file)
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def getImgWidthHeight(self, path):
        """Uses pil to image size in pixels.
        Params:
            path (string) : path to the image
        """
        if os.path.isfile(path):
            im = Image.open(path)
            return im.size
        return None
    
###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗        
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝        
 ██║  ███╗███████║██╔████╔██║█████╗          
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝          
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗        
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝        
                                             
 ███████╗██████╗ ██████╗ ██╗████████╗███████╗
 ██╔════╝██╔══██╗██╔══██╗██║╚══██╔══╝██╔════╝
 ███████╗██████╔╝██████╔╝██║   ██║   █████╗  
 ╚════██║██╔═══╝ ██╔══██╗██║   ██║   ██╔══╝  
 ███████║██║     ██║  ██║██║   ██║   ███████╗
 ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

"""
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

        super().__init__()

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface, missile=False):
        if not missile:
            self.position = wrap_position(self.position + self.velocity, surface)
        else:
            self.position = (self.position + self.velocity)

    def collides_with(self, other_obj, SHIELDS=False):
        if not SHIELDS:
            distance = self.position.distance_to(other_obj.position)
            return distance < (self.radius + other_obj.radius) - 50
        else:
            distance = self.position.distance_to(other_obj.position)
            return distance < (self.radius + other_obj.radius)

###################################################################################################
"""
  █████╗ ███████╗████████╗███████╗██████╗  ██████╗ ██╗██████╗ 
 ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔═══██╗██║██╔══██╗
 ███████║███████╗   ██║   █████╗  ██████╔╝██║   ██║██║██║  ██║
 ██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║   ██║██║██║  ██║
 ██║  ██║███████║   ██║   ███████╗██║  ██║╚██████╔╝██║██████╔╝
 ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ 
                                                              
"""
class Asteroid(GameSprite):
    def __init__(self, location, smsc_dimensions):
        self.IdleImageLink = r"Assets\Sprites\Asteroids\Explosion\0.png"
        self.Explosion_Frames = len(os.listdir("Assets\Sprites\Asteroids\Explosion"))
        self.Explosion_Frame = 0
        self.InOrbit = True
        self.Exploding = False
        self.Smoothscale=smsc_dimensions
        self.spriteObject = load_sprite(self.IdleImageLink, self.Smoothscale)
        self.ANGLE = random.randrange(0, 359, 3)
        self.direction = Vector2(UP)
        self.ACCELERATION = 0.75
        self.MAX_VELOCITY = 5

        ## Rotate by degrees in-place
        self.direction.rotate_ip(self.ANGLE)

        self.direction[0] = abs(self.direction[0])
        self.direction[1] = abs(self.direction[1])

        self.getUnitCircleQuadrant()

        GameSprite.__init__(self, location, self.spriteObject, Vector2(self.direction))

    ## Modified Unit Circle Trig Math
    def getUnitCircleQuadrant(self):
        if self.ANGLE >= 0 and self.ANGLE <= 90:
            ## Where X is negative and Y is negative
            self.direction[0] = self.direction[0] * -1
            self.direction[1] = self.direction[1] * -1
        elif self.ANGLE > 90 and self.ANGLE <= 180:
            ## Where X is negative and Y is positve
            self.direction[0] = self.direction[0] * -1
        elif self.ANGLE > 270 and self.ANGLE <= 359:
            ## Where X is positive and Y is negative
            self.direction[1] = self.direction[1] * -1

    def drawAsteroid(self, screen):
        if self.velocity.length() < self.MAX_VELOCITY:
            self.velocity += self.direction * self.ACCELERATION
        GameSprite.draw(self, screen)
        GameSprite.move(self, screen, False)

    def destroy(self):
        imageLink = f"Assets\Sprites\Asteroids\Explosion\{self.Explosion_Frame}.png"
        self.spriteObject = load_sprite(imageLink, self.Smoothscale)
        self.sprite = self.spriteObject

        if self.Explosion_Frame < self.Explosion_Frames - 1:
            self.Explosion_Frame += 1
        else:
            self.InOrbit = False
            self.kill() 

###################################################################################################
""" 
 ███████╗██╗  ██╗██╗███████╗██╗     ██████╗ ███████╗
 ██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗██╔════╝
 ███████╗███████║██║█████╗  ██║     ██║  ██║███████╗
 ╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║╚════██║
 ███████║██║  ██║██║███████╗███████╗██████╔╝███████║
 ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝ ╚══════╝
                                                    
"""
class Shields(GameSprite):
    def __init__(self, location):
        self.Shield_Frames = len(os.listdir("Assets\Sprites\Shields"))
        self.Shield_Frame = 0
        self.Location = location
        self.Smoothscale = (170,170)
        self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'
        self.SHIELD_HEALTH = 75
        self.SHIELDS_COOLDOWN = 100
        self.COOLING_DOWN = False

        self.spriteObject = load_sprite_rotated(self.imageLink, self.Smoothscale, 0)

        super().__init__(self.Location, self.spriteObject, Vector2(0))

    def updateFrames(self):
        if self.Shield_Frame < self.Shield_Frames - 1:
            self.Shield_Frame += 1
            self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject
        else:
            self.Shield_Frame = 0
            self.imageLink = f'Assets\Sprites\Shields\{self.Shield_Frame}.png'
            self.spriteObject = load_sprite(self.imageLink, self.Smoothscale)
            self.sprite = self.spriteObject

    def updateShields(self, usingShields):
        if self.COOLING_DOWN == False:
            if usingShields:
                if self.SHIELD_HEALTH > 0:
                    self.SHIELD_HEALTH -= 1
                else:
                    self.COOLING_DOWN = True
            else:
                if self.SHIELD_HEALTH < 75:
                    self.SHIELD_HEALTH += 1
        else:
            self.SHIELDS_COOLDOWN -= 1

        if self.SHIELDS_COOLDOWN == 0:
            self.COOLING_DOWN = False
            self.SHIELD_HEALTH = 76
            self.SHIELDS_COOLDOWN = 100

###################################################################################################
"""
  ██████╗  █████╗ ███╗   ███╗███████╗              
 ██╔════╝ ██╔══██╗████╗ ████║██╔════╝              
 ██║  ███╗███████║██╔████╔██║█████╗                
 ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝                
 ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗              
  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝              
                                                   
  ██████╗ ██████╗      ██╗███████╗ ██████╗████████╗
 ██╔═══██╗██╔══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
 ██║   ██║██████╔╝     ██║█████╗  ██║        ██║   
 ██║   ██║██╔══██╗██   ██║██╔══╝  ██║        ██║   
 ╚██████╔╝██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
  ╚═════╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   
                                                   
"""

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj, SHIELDS=False):
        if not SHIELDS:
            distance = self.position.distance_to(other_obj.position)
            return distance < (self.radius + other_obj.radius) - 50
        else:
            distance = self.position.distance_to(other_obj.position)
            return distance < (self.radius + other_obj.radius)

###################################################################################################
"""
 ███████╗██████╗  █████╗  ██████╗███████╗███████╗██╗  ██╗██╗██████╗ 
 ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝██║  ██║██║██╔══██╗
 ███████╗██████╔╝███████║██║     █████╗  ███████╗███████║██║██████╔╝
 ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝  ╚════██║██╔══██║██║██╔═══╝ 
 ███████║██║     ██║  ██║╚██████╗███████╗███████║██║  ██║██║██║     
 ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
                                                                    
"""
class Spaceship(GameObject):
    MANEUVERABILITY = 5
    ACCELERATION = 0.25
    Missile_SPEED = 50

    def __init__(self, position, Missile_callback=None, image ="space_ship_40x40.png"):
        self.Missile_callback = Missile_callback
        self.laser_sound = load_sound("fireEffect")
        self.tick = 0
        self.frame = 0
        self.frames = len(os.listdir("Assets\Spaceships\Idle"))
        self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.direction = Vector2(UP)
        self.ANGLE = 0
        self.HEALTH = 10
        self.Shields = False
        self.SpaceshipShields = Shields(tuple(position))

        super().__init__(position, load_sprite(self.image, (85,85)), Vector2(0))

    def __str__(self):
        """String version of this objects state"""
        attributes = {}
        attributes["ship_image"] = self.image
        attributes["position"] = (self.position.x, self.position.y)
        return json.dumps(attributes)

    def getAttributes(self):
        """
            Returns the basic attributes needed to set up a copy of this object
            possibly in a multiplayer setting.
        """
        return self.__str__()

    def getLocation(self):
         return tuple(self.position)
    
    def getShieldStatus(self):
        self.Shields = True
        return self.Shields
    
    def getVelocity(self):
        return self.velocity.x, self.velocity.y

    def drawHealthBar(self, screen):
        pygame.draw.rect(screen, self.RED, (self.position[0] - 25, self.position[1] + 50, 50, 10))
        pygame.draw.rect(screen, self.GREEN, (self.position[0] - 25, self.position[1] + 50, 50 - (5 * (10 - self.HEALTH)), 10))
    
    def drawShieldBar(self, screen):
        shield_font = pygame.font.SysFont('Algerian', 30)
        player_shield_text = shield_font.render(
                "Player Shields: " + str(self.SpaceshipShields.SHIELD_HEALTH), 1, (255,255,255))
        screen.blit(player_shield_text, (1180,10))

        shield_cooldown_font = pygame.font.SysFont('Algerian', 30)
        player_shield_cooldown_text = shield_cooldown_font.render(
                "Cooldown Time: " + str(self.SpaceshipShields.SHIELDS_COOLDOWN), 1, (255,255,255))
        screen.blit(player_shield_cooldown_text, (1180,45))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.ANGLE += self.MANEUVERABILITY * sign

        if self.ANGLE > 360:
            self.ANGLE -= 360
        elif self.ANGLE < 0:
            self.ANGLE += 360

        self.direction.rotate_ip(angle)

    def accelerate(self, velocity=None):
        if velocity != None:
            self.velocity = Vector2(velocity)
        else:
            self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        if self.tick % 3 == 0:
            if self.frame < self.frames - 1:
                self.frame += 1
                self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
                self.sprite = load_sprite(self.image, (85,85))
            else:
                self.frame = 0
                self.image = f"Assets\Spaceships\Idle\{self.frame}.png"
                self.sprite = load_sprite(self.image, (85,85))
        self.tick += 1
        angle = self.direction.angle_to(UP)
        rotated_surface = transform.rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        self.SpaceshipShields.Location = self.position
        
        if self.Shields:
            if self.SpaceshipShields.COOLING_DOWN == False:
                self.SpaceshipShields.draw(surface)
                self.SpaceshipShields.updateFrames()
                self.SpaceshipShields.updateShields(self.Shields)
                self.Shields = False
                self.SpaceshipShields.position = self.getLocation()
            else:
                self.SpaceshipShields.updateShields(self.Shields)


    def shoot(self):
        Missile_velocity = self.direction * self.Missile_SPEED + self.velocity
        missile = Missile(tuple(self.position), Missile_velocity, self.ANGLE)
        self.Missile_callback(missile)
        self.laser_sound.play()

###################################################################################################
""" 
 ███╗   ███╗██╗███████╗███████╗██╗██╗     ███████╗
 ████╗ ████║██║██╔════╝██╔════╝██║██║     ██╔════╝
 ██╔████╔██║██║███████╗███████╗██║██║     █████╗  
 ██║╚██╔╝██║██║╚════██║╚════██║██║██║     ██╔══╝  
 ██║ ╚═╝ ██║██║███████║███████║██║███████╗███████╗
 ╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝╚══════╝╚══════╝
                                                  
"""                                                           
class Missile(GameObject):
    def __init__(self, position, velocity, firingAngle):
        self.frame = 0
        self.frames = len(os.listdir("Assets\Sprites\Projectile"))
        self.ANGLE = firingAngle
        self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"

        super().__init__(position, load_sprite_rotated(self.imageLink, (100,100), firingAngle), velocity)

        self.tick = 0

    def move(self, surface):
        self.tick += 1
        self.position = self.position + self.velocity

        if self.tick % 2 == 0:

            if self.frame < self.frames - 1:
                self.frame += 1
                self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"
                self.sprite = load_sprite_rotated(self.imageLink, (100,100), self.ANGLE)
            else:
                self.frame = 0
                self.imageLink = f"Assets\Sprites\Projectile\{self.frame}.png"
                self.sprite = load_sprite_rotated(self.imageLink, (100,100), self.ANGLE)
