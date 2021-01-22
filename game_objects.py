import random
import copy
import pygame
from dataclasses import dataclass, field
from time import sleep


@dataclass
class GameWindow:
    """
    Create an object of this class to put a snake
    The look and feel of the game window is decided by this class
    """
    
    SCREEN_WIDTH:int = 500
    SCREEN_HEIGHT:int = 500
    BG_COLOR:tuple = (255,255,255)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pygame.font.init()
    msg_font = pygame.font.SysFont("Comic Sans MS", 20)
    score_font = pygame.font.SysFont('Raleway', 20, bold=True)
    
    def display_text(self, text, position = None, color=None , font_type=None):
        """
        call this funtion to write a text on the game window
        """
        if position == None:
            position = (self.SCREEN_WIDTH/4, self.SCREEN_HEIGHT/4)
        if color == None:
            color = (100,100,100)
        if font_type == None:
            font_type = self.msg_font
        
        label = font_type.render(text, 1, color)
        self.screen.blit(label, position)

    def display_score(self,score):
        """
        A simple text displayed on any one corner of the game window
        """
        x = self.SCREEN_WIDTH - 100
        y = 10
        position = (x,y)
        score_text = 'Score : ' + str(score)
        self.display_text(score_text, position=position,font_type = self.score_font)



@dataclass
class UnitCell:
    """
    A single cell that can be used both as food and snake's body
    """
    x:int
    y:int
    size:int
    color:tuple = (0,0,255)

    def __post_init__(self):
        self.position = [self.x, self.y]
        self.rect = pygame.Rect((self.position ), (self.size*2, self.size*2))
        self.rect.center = (self.position )


class Food(UnitCell):
    """
    Food extends UnitCell and positions on the game window randomly
    """
    def __init__(self,x,y,size = 5,food_color=(255,0,0)):
        super().__init__(x=x, y=y, size = size, color=food_color)

@dataclass
class Snake:
    """
    Object of class Snake can be created and put on a pygame window
    Snake is made up of new cells (UnitCell) and stored in an array
    """
    starting_position:tuple
    cell_size:int=5
    moving_direction:str = 'right'
    #velocity:int=5
    color:tuple = (0,0,255)
    body = []
    tail = None
    old_tail = None

    def __post_init__(self):
        self.cell_gap = self.cell_size*2.2
        self.head = self.make_new_cell(x=self.starting_position[0],
                            y=self.starting_position[1])
        
        self.body.append(self.head) #last cell in body is always head

    def make_new_cell(self, x, y, size=None, color=None):
        if size == None:
            size = self.cell_size
        if color == None:
            color = self.color
        new_cell = UnitCell(x=x, y=y, size=size, color=color)

        return new_cell

    def add_new_cell_to_head(self,cell:UnitCell):
        """
        Increase the size of the snake by adding cells
        """
        new_cell = self.make_new_cell(x=cell.x, y=cell.y)
        self.body.append(new_cell)
        self.update_head()


    def update_head(self):
        self.head = self.body[-1]


    def move(self, direction):
        self.moving_direction = direction
        # create a new cell in the moving direction and attacht it to the body
        current_head = self.body[-1]
        new_x, new_y = current_head.position
        if direction == "left":
            new_x -= self.cell_gap 
        if direction == "right":
            new_x += self.cell_gap 
        if direction == "up":
            new_y -= self.cell_gap 
        if direction == "down":
            new_y+= self.cell_gap 
        #transition from existing head to new cell in the moving direction
        new_head = self.make_new_cell(x=new_x, y=new_y,)
        self.body.append(new_head)
        self.old_tail = self.body.pop(0)
        self.tail = self.body[0]
        self.update_head()

    def reset(self):
        """
        reset will destroy body and move the head to starting position
        """
        self.body = []
        self.__post_init__()

