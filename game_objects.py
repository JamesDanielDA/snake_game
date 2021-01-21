import random
import copy
import pygame
from dataclasses import dataclass, field
from time import sleep


@dataclass
class GameWindow:
    """
    Create an object of this class to put a snake
    The look and feel of the game is decided by this class
    """
    
    SCREEN_WIDTH:int = 500
    SCREEN_HEIGHT:int = 500
    BG_COLOR:tuple = (255,255,255)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


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
    Snake will keep a record of its own body parts in relationship with window coordinates
    pygame captures keystrokes from the player and passes it to Snake which in turn decides all the manouvers 
    """
    starting_position:tuple
    cell_size:int=5
    moving_direction:str = 'right'
    velocity:int=5
    color:tuple = (0,0,255)

    def __post_init__(self):
        self.has_collided=False
        self.body = []
        self.tail = None
        self.old_tail = None
        self.head = self.make_new_cell(x=self.starting_position[0],
                            y=self.starting_position[1])
        
        self.body.append(self.head) #last cell in body is always head
        #define all four boundaries relative to the center coordinates of sneak's cell

    def make_new_cell(self, x, y, size=None, color=None):
        if size == None: size = self.cell_size
        if color == None: color = self.color
        new_cell = UnitCell(x=x,
                                y=y,
                                size=size,
                                color=color)
        return new_cell

    def add_new_cell_to_head(self,cell:UnitCell):
        """
        Increase the size of the snake by adding cells
        """
        self.body.append(cell)
        self.update_head()


    def update_head(self):
        self.head = self.body[-1]


    def move(self, direction):
        self.moving_direction = direction
        # create a new cell in the moving direction and attacht it to the body
        current_head = self.body[-1]
        new_x, new_y = current_head.position
        if direction == "left":
            new_x -= self.velocity
        if direction == "right":
            new_x += self.velocity
        if direction == "up":
            new_y -= self.velocity
        if direction == "down":
            new_y+= self.velocity
        #make and add new head and remove tail from body
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

