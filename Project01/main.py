# /*****************************************************************************
# *                    
# *  Author:           Deangelo Brown
# *  Email:            deangelobrown808@gmail.com
# *  Label:            A01
# *  Title:            2048 Game
# *  Course:           CMPS 5443
# *  Semester:         Spring 2023
# * 
# *  Description:
# *        This program will use python's pygame to create 2048. 2048 is a puzzle base game where 
# *        the goal is to slide numbered tiles on a grid to combine them to create a tile with the   
# *        number 2048. Using pygame we will attempt to simulate that game.
# *  References:
# *           https://github.com/rugbyprof/5443-2D-Gaming/tree/main/Assignments/02-P01/helper_code/2048      
# *           https://stackoverflow.com/questions/4056768/how-to-declare-array-of-zeros-in-python-or-an-array-of-a-certain-size
# *           https://www.pygame.org/docs/
# *         
# *        
# *  Usage: 
# *       - $ ./main filename
# *       - This will allow to run the program
# *       
# *  Files:            
# *       main.py    : driver program 
# *       music1.mp3 : Game background music
# *       color.py   : File with all colors
# *****************************************************************************/

import pygame
import random
import moviepy.editor


#Initialize Pygame
pygame.init()

"""
Setting the window size of the screen and defining other variables to be later used.

"""

WIDTH = 400      
HEIGHT = 500

running = True

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048 Gaming')           #Displays Caption
icon = pygame.image.load("log.png")                 #Loads Logo
pygame.display.set_icon(icon)
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()



padding = 20                                        #Creates padding between cells
size_for_pieces = 95                                #Size for each "Block" to hold 0
cell_size = 75                                      
center_point = 57                                   #Center point of the blocks

full_board = False                                  #Keeps track if the board is full 
add_new = True                                      
matrix = [[0 for _ in range(4)] for _ in range(4)]  #Creates the initial game matrix and loads them with the value 0
first_2 = 0                                         #Sets first 2 as you load game to 0
score = 0

pressed_key = None



""""
Sample Colors for game
"""
ALICEBLUE = (240, 248, 255)
ANTIQUEWHITE = (250, 235, 215)
AQUA = (0, 255, 255)
AQUAMARINE = (127, 255, 212)
AZURE = (240, 255, 255)
BEIGE = (245, 245, 220)
BISQUE = (255, 228, 196)
BLACK = (0, 0, 0)
BLANCHEDALMOND = (255, 235, 205)
BLUE = (0, 0, 255)
BLUEVIOLET = (138, 43, 226)
BRIGHTRED = (255, 0, 0)

#Referenced colors
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (127, 255, 212),
    32: (255, 105, 180),
    64: (240, 230, 140),
    128: (32, 178, 170),
    256: (128, 128, 0),
    512: (175, 238, 238),
    1024: (219, 112, 147),
    2048: (102, 51, 153),
    'luminous': (249, 246, 242),
    'dim': (119, 110, 101),
    'basic': (0, 0, 0),
}

class Move:
    """
    Simple class which contains all of the move functions for 2048. Uses the sample functions provided in class adjusting them
    to make it easier to iteraterate through the matrix. Each function operates similarly tweeking the row and col variable based on
    the moves made Up, Down, Left, Right.
    
    
    """

    def __init__(self, matrix):
        self.matrix = matrix
        self.merged = [[False for _ in range(len(self.matrix))] for _ in range(len(self.matrix))]
        self.score = 0
    
    def move_up(self):

        global score
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                shift = 0
                if row > 0:
                    for temp in range(row):
                        if self.matrix[temp][col] == 0:
                            shift +=1
                    if shift > 0:
                        self.matrix[row - shift][col] = self.matrix[row][col]
                        self.matrix[row][col] = 0

                    if self.matrix[row - shift - 1][col] == self.matrix[row - shift][col] and not self.merged[row - shift][col] and not self.merged[row - shift - 1][col]:
                            self.matrix[row - shift - 1][col] =self.matrix[row - shift - 1][col] * 2
                            score += self.matrix[row - shift - 1][col]
                            self.matrix[row - shift][col] = 0
                            self.merged[row - shift - 1][col] = True
        
        return self.matrix
               


    def move_down(self):
        global score
        for row in range(len(self.matrix) - 1):
            for col in range(len(self.matrix)):
                shift = 0
                for temp in range(row + 1):
                    if self.matrix[(len(self.matrix)-1) - temp][col] == 0:
                        shift += 1
                if shift > 0:
                    self.matrix[(len(self.matrix)-2) - row + shift][col] = self.matrix[(len(self.matrix)-2) - row][col]
                    self.matrix[(len(self.matrix)-2) - row][col] = 0
                if 3 - row + shift <= 3:
                    if self.matrix[(len(self.matrix)-2) - row + shift][col] == self.matrix[(len(self.matrix)-1) - row + shift][col] and not self.merged[(len(self.matrix)-1) - row + shift][col] and not self.merged[(len(self.matrix)-2) - row + shift][col]:
                        self.matrix[(len(self.matrix)-1) - row + shift][col] =self.matrix[(len(self.matrix)-1) - row + shift][col] * 2
                        score += self.matrix[(len(self.matrix)-1) - row + shift][col]
                        self.matrix[(len(self.matrix)-2) - row + shift][col] = 0
                        self.merged[(len(self.matrix)-1) - row + shift][col] = True 

        
        return self.matrix


    def move_right(self):
        
        global score
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix) - 1):
                shift = 0
                for temp in range(col):
                    if self.matrix[row][(len(self.matrix)-1) - temp] == 0:
                        shift += 1
                if shift > 0:
                    self.matrix[row][(len(matrix)-1) - col + shift] = self.matrix[row][(len(self.matrix)-1) - col]
                    self.matrix[row][(len(matrix)-1) - col] = 0
                if 3 - row + shift <= 3:
                    if self.matrix[row][(len(self.matrix)-2) - col + shift] == self.matrix[row][(len(self.matrix)-1) - col + shift] and not self.merged[row][(len(self.matrix)-1) - col + shift] and not self.merged[row][(len(self.matrix)-2) - col + shift]:
                        self.matrix[row][(len(self.matrix)-1) - col + shift] =self.matrix[row][(len(self.matrix)-1) - col + shift] * 2
                        score += self.matrix[row][(len(self.matrix)-1) - col + shift]
                        self.matrix[row][(len(self.matrix)-2) - col + shift] = 0
                        self.merged[row][(len(self.matrix)-1) - col + shift] = True 


        return self.matrix




    def move_left(self):
  
        global score
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                shift = 0
                for temp in range(col):
                    if self.matrix[row][temp] == 0:
                        shift +=1
                    if shift > 0:
                        self.matrix[row][col - shift] = self.matrix[row][col]
                        self.matrix[row][col] = 0
                    if self.matrix[row][col - shift] == self.matrix[row][col - shift - 1] and not self.merged[row][col - shift] and not self.merged[row][col - shift - 1]:
                        self.matrix[row][col - shift - 1] = self.matrix[row][col - shift - 1] * 2
                        score += self.matrix[row][col - shift - 1]
                        self.matrix[row][col - shift] = 0
                        self.merged[row][col - shift - 1] = True
                    


        return self.matrix


    
"""
Creates game feild as a 4x4 matrix to mimic 2048.
Creates the boxes that house the values that change colors based on their numbers
Addes padding between each box and renders the numbers in the center point

"""

def create_game_feild(feild):
    for row in range(len(feild)):
        box_x = row * size_for_pieces + padding
        for col in range(len(feild)):
            box_y = col * size_for_pieces + padding
            temp = feild[row][col]
            if temp > 8:
                temp_color = colors['luminous']
            else:
                temp_color = colors['dim']
            if temp <= 2048:
                color = colors[temp]
            else:
                color = colors['basic']
            pygame.draw.rect(screen, color, pygame.Rect(box_y, box_x, cell_size, cell_size), 0,5)
            if temp > 0:
                number = len(str(temp))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * number))
                number_display = font.render(str(temp), True, temp_color)
                number_box = number_display.get_rect(center=(col * size_for_pieces + center_point, row * size_for_pieces + center_point))
                screen.blit(number_display, number_box)



#Adds a new 2 to the feild after event is called
def add_new_2(matrix):
    count = 0
    full_board = False

    while any(0 in row for row in matrix) and count < 1:
        row = random.randint(0,3)
        col = random.randint(0,3)
        if matrix[row][col] == 0:
            count +=1
            matrix[row][col] = 2


    if count < 1:
        full_board = True
    return matrix, full_board   


#Keeps track of the current state of the game to determine whether a player has won or lost the game
def get_current_state(matrix):
    
    game_done =  False
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if matrix[row][col] == 2048:
                imp = pygame.image.load("winner.jpg").convert()
                img = pygame.transform.scale(imp, (400, 500))
                game_done = True
                pygame.draw.rect(screen, (0,0,0), [50, 50, 300, 100], 0, 10)
                screen.fill((169,169,169))
                screen.blit(img, (0, 0))
            if(matrix[row][col]== matrix[row + 1][col] or matrix[row][col]== matrix[row][col + 1]):
                return matrix
            if(matrix[row][col]== matrix[row - 1][col] or matrix[row][col]== matrix[row][col - 1]):
                return matrix
            else:
                imp = pygame.image.load("defeat.jpg").convert()
                img = pygame.transform.scale(imp, (400, 500))
                game_done = False
                pygame.draw.rect(screen, (0,0,0), [50, 50, 300, 100], 0, 10)
                screen.fill((169,169,169))
                screen.blit(img, (0, 0))



            return game_done


#Loads background music from mp3 file and plays its for the duration of the game
pygame.mixer.music.load("music1.mp3")
pygame.mixer.music.play()       

#Create a button for the user to reset the game
font = pygame.font.SysFont("Georgia", 15, bold=True)
reset = font.render("Reset Game", True, "white")
button = pygame.Rect(5, 430, 110,40)






while running:
    timer.tick(60)
    screen.fill('grey')
    pygame.draw.rect(screen,(187, 173, 160), [0,0,400,400], 0, 10)
    create_game_feild(matrix)
    game = Move(matrix)
    
    
    keep_score = font.render(f'Score: {score}', True, 'white')
    screen.blit(keep_score, (10, 405))
    

    if add_new or first_2 < 2:
        matrix, full_board  = add_new_2(matrix)
        add_new = False
        first_2 +=1
    
    if full_board:
        get_current_state(matrix)

    if pressed_key:
        if pressed_key == 1:
            matrix = game.move_up()
            pressed_key = None
            add_new = True
        elif pressed_key == 2:
            matrix = game.move_down()
            pressed_key = None
            add_new = True
        elif pressed_key == 3:
            matrix = game.move_right()
            pressed_key = None
            add_new = True
        elif pressed_key == 4:
            matrix = game.move_left()
            pressed_key = None
            add_new = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                matrix = [[0 for _ in range(4)] for _ in range(4)]
                add_new= True
                first_2 = 0
                score = 0
                pressed_key = None
                full_board = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                print('UP')
                pressed_key = 1
            elif event.key == pygame.K_DOWN:
                print('DOWN')
                pressed_key = 2
            elif event.key == pygame.K_RIGHT:
                print('RIGHT')  
                pressed_key = 3
            elif event.key == pygame.K_LEFT:
                print('LEFT')  
                pressed_key = 4
            elif event.key == pygame.K_SPACE:
                matrix = [[0 for _ in range(4)] for _ in range(4)]
                add_new= True
                first_2 = 0
                score = 0
                pressed_key = None
                full_board = False
            elif event.key == pygame.K_w:
                imp = pygame.image.load("winner.jpg").convert()
                img = pygame.transform.scale(imp, (400, 500))
                game_done = True
                pygame.draw.rect(screen, (0,0,0), [50, 50, 300, 100], 0, 10)
                screen.fill((169,169,169))
                #screen.blit(img, (150, 150))
                screen.blit(img, (0, 0))
            elif event.key == pygame.K_e:
                imp = pygame.image.load("defeat.jpg").convert()
                img = pygame.transform.scale(imp, (400, 500))
                game_done = False
                pygame.draw.rect(screen, (0,0,0), [50, 50, 300, 100], 0, 10)
                screen.fill((169,169,169))
                screen.blit(img, (0, 0))
                
            
            if full_board:
                if event.key == pygame.K_SPACE:
                    matrix = [[0 for _ in range(4)] for _ in range(4)]
                    add_new= True
                    first_2 = 0
                    score = 0
                    pressed_key = None
                    full_board = False
        
        x_corrdinate,y_corrdinate = pygame.mouse.get_pos()
        if button.x <= x_corrdinate <= button.x + 90 and button.y <= y_corrdinate <= button.y + 60:
            pygame.draw.rect(screen, 'grey', button)
            pass
        else:
            pygame.draw.rect(screen, (187, 173, 160), button)
        screen.blit(reset,(button.x + 5, button.y + 5 ))



        pygame.display.update()
        
    
    
        #pygame.display.flip()
pygame.quit()