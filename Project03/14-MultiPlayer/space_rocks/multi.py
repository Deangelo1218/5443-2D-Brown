import pygame

from models import Asteroid, Spaceship, Background
from utils import get_random_position, load_sprite, print_text, load_sound
from random import shuffle
import ast
import messenger
from pygame import mixer

import pygame
import math
import random
from pygame.math import Vector2
import sys
import os


""" 
    ███████╗██████╗  █████╗  ██████╗███████╗ 
    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝ 
    ███████╗██████╔╝███████║██║     █████╗   
    ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝   
    ███████║██║     ██║  ██║╚██████╗███████╗ 
    ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝ 
                                            
    ██████╗  ██████╗  ██████╗██╗  ██╗███████╗
    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝██╔════╝
    ██████╔╝██║   ██║██║     █████╔╝ ███████╗
    ██╔══██╗██║   ██║██║     ██╔═██╗ ╚════██║
    ██║  ██║╚██████╔╝╚██████╗██║  ██╗███████║
    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝
                                            
"""
class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self, multiplayer=None):
        self._init_pygame()
        self.width = 1500
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))

        ## Background Stuff
        self.tick = 0
        self.BG_Frames = len(os.listdir("Assets/Background/Stars"))
        self.BG_Frame = 0
        self.RS_Frames = len(os.listdir("Assets/Background/RotaryStar"))
        self.RS_Frame = 0
        self.BH_Frames = len(os.listdir("Assets/Background/BH"))
        self.BH_Frame = 0
        self.ASTEROIDS_DESTROYED = 0
        self.ASTEROID_ATTACK_COUNTDOWN = 20
        self.ATTACK = False

        ## Asteroid Stuff
        self.Locations = [(100,150),(300,300),(500,200),(1300,200),
                                   (1100,600),(700,700),(1450,620),(650,150),
                                   (1450,850),(900,800),(100,620),(150,150),
                                   (1420,100),(100,800),(1100,120),(150,850)]
        
        self.ASTEROID_COUNT = len(self.Locations)
        self.explosion = load_sound("explosion")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        """
        Colors = [(251,250,245),(199,206,250),(255,255,186),(186,225,255),
        (181,234,215),(255,183,178),(226,240,203),(224,187,228),(229,204,255),
        (236,221,185)]
        self.__color = Colors[player] 
        """

        self.__host = False

        self.asteroids = []
        self.Missiles = []
        self.spaceship = Spaceship(
            (random.randrange(100, self.screen.get_width() - 100), random.randrange(100, self.screen.get_height() - 100)), self.Missiles.append
        )

        self.__messenger = multiplayer


        if multiplayer != None:
            self.__messenger.setCallback(self.__receiveMessage)

            self.__sendMessage(
                {'Type': 'Who'}
            )

            self.__sendMessage(
                {'Type': 'Join',
                 'Message': self.__messenger.user + ' has joined the game!',
                 'Ship': [self.spaceship.getLocation()]
                 }
            )
            self.__playerIds = []

        self.__otherPlayers = []
        self.__allPlayers = [self.spaceship]

        self.npcs = []

        self.started = False

        for index, item in enumerate(self.Locations):
            self.asteroids.append(Asteroid(item, (150,150)))
    

    def updateFrames(self):
        if self.BG_Frame < self.BG_Frames - 1:
            self.BG_Frame += 1
        else:
            self.BG_Frame = 0
        if self.RS_Frame < self.RS_Frames - 1:
            self.RS_Frame += 1
        else:
            self.RS_Frame = 0
        if self.BH_Frame < self.BH_Frames - 1:
            self.BH_Frame += 1
        else:
            self.BH_Frame = 0



    """
            ███╗   ███╗ █████╗ ██╗███╗   ██╗                  
            ████╗ ████║██╔══██╗██║████╗  ██║                  
            ██╔████╔██║███████║██║██╔██╗ ██║                  
            ██║╚██╔╝██║██╔══██║██║██║╚██╗██║                  
            ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║                  
            ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝                  
                                            
            ██╗      ██████╗  ██████╗ ██████╗ 
            ██║     ██╔═══██╗██╔═══██╗██╔══██╗
            ██║     ██║   ██║██║   ██║██████╔╝
            ██║     ██║   ██║██║   ██║██╔═══╝ 
            ███████╗╚██████╔╝╚██████╔╝██║     
            ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     
                                                
 
    """
    def main_loop(self):
        pygame.mixer.music.load("game.mp3")
        pygame.mixer.music.play()     
     

        while True:
            self._handle_input()
            if self.started:
                self._process_game_logic()
            self._draw()

            if self.tick % 3 == 0:
                self.updateFrames()
            self.tick += 1
            

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroid Destroyer")


    """
            ██╗  ██╗ █████╗ ███╗   ██╗██████╗ ██╗     ███████╗     
            ██║  ██║██╔══██╗████╗  ██║██╔══██╗██║     ██╔════╝     
            ███████║███████║██╔██╗ ██║██║  ██║██║     █████╗       
            ██╔══██║██╔══██║██║╚██╗██║██║  ██║██║     ██╔══╝       
            ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗███████╗     
            ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚══════╝     
                                                        
                 ██╗███╗   ██╗██████╗ ██╗   ██╗████████╗
                 ██║████╗  ██║██╔══██╗██║   ██║╚══██╔══╝
                 ██║██╔██╗ ██║██████╔╝██║   ██║   ██║   
                 ██║██║╚██╗██║██╔═══╝ ██║   ██║   ██║   
                 ██║██║ ╚████║██║     ╚██████╔╝   ██║   
                 ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝    ╚═╝   
                                                        
    """
    def _handle_input(self):

        sendMessage = False
        Message = {
            'Type': 'Event',
            'Events': []
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()
                sendMessage = True
                Message['Events'].append({'Type': 'Shoot'})
                
            if event.type == pygame.KEYUP:
                pass
                #print("key released send message")

        is_key_pressed = pygame.key.get_pressed()
        
        
        if not self.started:
            if is_key_pressed[pygame.K_g]:
                self.started = True

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
                sendMessage = True
                Message['Events'].append({'Type': 'Rotate', 'Clockwise': 1})
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
                sendMessage = True
                Message['Events'].append({'Type': 'Rotate', 'Clockwise': 0})
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
                sendMessage = True
                Message['Events'].append({'Type': 'Accelerate'})
                if len(self.npcs) > 0:
                    for npc in self.npcs:
                        npc.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(0)
                sendMessage = True
                Message['Events'].append({'Type': 'Stop'})

            if is_key_pressed[pygame.K_RSHIFT]:
                self.spaceship.Shields = True
                sendMessage = True
                Message['Events'].append({'Type': 'Shield'})

            if sendMessage == True:
                self.__sendMessage(Message)



    """
         ██████╗  █████╗ ███╗   ███╗███████╗    ██╗      ██████╗  ██████╗ ██╗ ██████╗
        ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██║     ██╔═══██╗██╔════╝ ██║██╔════╝
        ██║  ███╗███████║██╔████╔██║█████╗      ██║     ██║   ██║██║  ███╗██║██║     
        ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██║   ██║██║   ██║██║██║     
        ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ███████╗╚██████╔╝╚██████╔╝██║╚██████╗
         ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝ ╚═════╝
                                                                                    
    """
    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            if game_object:
                try:
                    game_object.drawAsteroid(self.screen)
                except:
                    game_object.move(self.screen)

        
        if self.spaceship:
            if self.ATTACK:
                for asteroid in self.asteroids:
                    if asteroid.collides_with(self.spaceship, self.spaceship.Shields):

                        asteroid.velocity *= -1

                        if self.spaceship.Shields == False:
                            self.spaceship.HEALTH -= 1

                            if self.spaceship.HEALTH< 1:
                                self.spaceship = None
                                self.message = "You lost!"
                                break

        for Missile in self.Missiles[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.Exploding == False:
                    if asteroid.collides_with(Missile):
                        self.ASTEROID_COUNT -= 1
                        self.ASTEROIDS_DESTROYED += 1
                        asteroid.Exploding = True
                        self.explosion.play()
                        self.Missiles.remove(Missile)
                        break

        for asteroid in self.asteroids[:]:
            if asteroid.InOrbit:
                if asteroid.Exploding:
                    asteroid.destroy()
            else:
                self.asteroids.remove(asteroid)

        for Missile in self.Missiles[:]:
            print(Missile)
            if not self.screen.get_rect().collidepoint(Missile.position):
                self.Missiles.remove(Missile)

        if self.ASTEROID_COUNT < 6:
            shuffle(self.Locations)

            for index, item in enumerate(self.Locations):
                self.asteroids.append(Asteroid(item, (150,150)))
                self.ASTEROID_COUNT += 1

        if not self.ATTACK:
            self.ASTEROID_ATTACK_COUNTDOWN -= 1
            if self.ASTEROID_ATTACK_COUNTDOWN == 0:
                self.ATTACK = True



    """
        ██████╗ ██████╗  █████╗ ██╗    ██╗
        ██╔══██╗██╔══██╗██╔══██╗██║    ██║
        ██║  ██║██████╔╝███████║██║ █╗ ██║
        ██║  ██║██╔══██╗██╔══██║██║███╗██║
        ██████╔╝██║  ██║██║  ██║╚███╔███╔╝
        ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ 
                                        
    """
    def _draw(self):

        self.screen.fill((0, 0, 0))

        StarryBackground = Background(f"Assets/Background/Stars/{self.BG_Frame}.png", [0, 0], (self.width, self.height))
        self.screen.blit(StarryBackground.image, StarryBackground.rect)

        RotaryStar1 = Background(f'Assets/Background/RotaryStar/{self.RS_Frame}.png', [210,500], (100,100))
        self.screen.blit(RotaryStar1.image, RotaryStar1.rect)

        RotaryStar2 = Background(f'Assets/Background/RotaryStar/{self.RS_Frame}.png', [1210,110], (100,100))
        self.screen.blit(RotaryStar2.image, RotaryStar2.rect)

        Blackhole = Background(f'Assets/Background/BH/{self.BH_Frame}.png', [815,350], (150,150))
        self.screen.blit(Blackhole.image, Blackhole.rect)

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.spaceship:
            self.spaceship.drawHealthBar(self.screen)
            self.spaceship.drawShieldBar(self.screen)
        
        self.drawAsteroidKills(self.screen)


        pygame.display.flip()
        self.clock.tick(60)


    def drawAsteroidKills(self, screen):
        kill_font = pygame.font.SysFont('Algerian', 30)
        player_kills_text = kill_font.render(
                "Team Asteroid Kills: " + str(self.ASTEROIDS_DESTROYED), 1, (255,255,255))
        screen.blit(player_kills_text, (10,10))



    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.Missiles]

        if self.spaceship:
            game_objects.append(self.spaceship)

        for player in self.__otherPlayers:
            game_objects.append(player)

        if len(self.npcs) > 0:
            for npc in self.npcs:
                game_objects.append(npc)

        return game_objects
    

    def __receiveMessage(self, ch, method, properties, body):
        """
        Receives messages from the server and handles them
        
        Parameters
        ----------
            ch : channel
            method :
            properties :
            body : json
        """
        #print(body)
        #converts bytes to dictionary
        bodyDic = ast.literal_eval(body.decode('utf-8'))
        #print(bodyDic)

        #if a player joins and they aren't yourself (broadcast also sends to self) and they aren't already in the game
        if bodyDic['Type'] == 'Join' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] not in self.__playerIds:
            #print('\n' + str(bodyDic['Message']))
            
            self.__otherPlayers.append(Spaceship(bodyDic['Ship'][0], self.Missiles.append))

            # append(Ship(bodyDic['Ship'][0], len(self.__otherPlayers)+1, bodyDic['Ship'][1]))
            self.__allPlayers.append(Spaceship(bodyDic['Ship'][0], self.Missiles.append))
            

            self.__playerIds.append(bodyDic['from'])
            #print(bodyDic['from'])
         

        #if someone joins the game and requests what users are already in the game
        elif bodyDic['Type'] == 'Who' and bodyDic['from'] != self.__messenger.user:
            if len(self.__playerIds) == 0 and self.__host == False:
                self.__host = True
                #self.__asteroids = [Asteroid(self.__screen, 3), Asteroid(self.__screen, 3)]

            self.__sendMessage({'Type': 'Join',
                                'Message': self.__messenger.user + ' is in the game!',
                                'Ship': [self.spaceship.getLocation()]})
     
        elif bodyDic['Type'] == 'Event' and bodyDic['from'] != self.__messenger.user and bodyDic['from'] in self.__playerIds:
            print(bodyDic)
            for dics in bodyDic['Events']:
                #if player accelerates accelerate the given ship 
                if dics['Type'] == 'Accelerate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].accelerate()
                if dics['Type'] == 'Rotate':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].rotate(clockwise=bool(dics['Clockwise']))
                if dics['Type'] == 'Shoot':
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].shoot()
                if dics['Type'] == 'Stop':  
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].accelerate(0)
                if dics['Type'] == 'Shield':  
                    self.__otherPlayers[self.__playerIds.index(bodyDic['from'])].getShieldStatus()
                    
            
            
    def __sendMessage(self, bodyDic):
        """
        Sends a message to the server
        
        Parameters
        ----------
            bodyDic : dictionary
        """
        self.__messenger.send("broadcast", bodyDic)
