"""
    Author:   Byron Dowling, Deangelo Brown, Izzy Olaemimimo
    Class:    5443 2D Python Gaming

    Asset Credits:

        Space Environment Sprites:
            - Author: [FoozleCC]
            - https://foozlecc.itch.io/void-fleet-pack-2
            - https://foozlecc.itch.io/void-environment-pack
            - https://foozlecc.itch.io/void-main-ship 
            - https://norma-2d.itch.io/celestial-objects-pixel-art-pack

"""
from multi import SpaceRocks
from messenger import Messenger
import sys

"""
    Example Run commands:
        python ex_05.py game1 player-1 'player-12023!!!!!'

        python .\__main__.py  game-01 player-01 'player-022023!!!!!'
        python .\__main__.py  game-01 player-02 'player-022023!!!!!'
"""
if len(sys.argv) < 3:
    print("Need: exchange and player ")
    print("Example: python ex05.py game-01 player-02")
    sys.exit()

game = sys.argv[1]
player = sys.argv[2]
creds = {
    "exchange": game,
    "port": "5672",
    "host": "terrywgriffin.com",
    "user": player,
    "password": player + "2023!!!!!",
}

if __name__ == "__main__":

    multiplayer = Messenger(creds)
    space = SpaceRocks(multiplayer)
    space.main_loop()
