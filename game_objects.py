import random
import pygame
from dataclasses import dataclass, field
from logger import GameLogger
from icons import icon_dict


log = GameLogger(file_dunder_name=__name__)

@dataclass
class GameWindow:
    """
    Create an object of this class to display the main game window
    :param SCREEN_WIDTH (int)           : width of the game window
    :param SCREEN_HEIGHT (int)          : height of the game window
    :param BG_COLOR (tuple[int,int,int]): background color of the main window
    :param panel_height (int)           : height of the panel that will appear on the bottom of the game window
    """
    
    SCREEN_WIDTH:int = 500
    SCREEN_HEIGHT:int = 500
    BG_COLOR:tuple = (200,200,200)
    panel_height = 40

    def __post_init__(self) -> None:
        self.screen = pygame.display.set_mode([self.SCREEN_WIDTH, self.SCREEN_HEIGHT + self.panel_height])
        self.surface= pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT + self.panel_height))
        self.surface.fill(self.BG_COLOR)
        #self.surface.set_alpha(0)

        pygame.font.init()
        self.msg_font = pygame.font.SysFont("Comic Sans MS", 20)
        self.score_font = pygame.font.SysFont('Raleway', 20, bold=True)
        pygame.display.set_caption('Snake Game')

        self.add_panel()
        self.add_border()
        log.logger.info(f'Created GameWindow:  {self.__dict__}')
    
    def render_background(self, image:pygame.Surface)-> None:
        """
        Callback function for the features on the bottom of the game window
        :param image (pygame.Surface) : this image will be set as the new background
        :return : None
        """

        self.surface.fill(self.BG_COLOR)
        self.surface.blit(image,(0,0))
        self.add_panel()
        self.add_border()
    
    def add_border(self)-> None:
        """
        Adds four boarders on the four sides of the window surface
        :return : None
        """

        color = (135, 62, 35)
        thickness = 3
        vertical_size = (thickness,self.SCREEN_HEIGHT)
        horizontal_size = (self.SCREEN_WIDTH,thickness)
        left_pos, right_pos = (0,0) , (self.SCREEN_WIDTH-thickness, 0)
        top_pos, bottom_pos = (0,0), (0,self.SCREEN_HEIGHT-thickness)
        
        border_left = pygame.Rect(left_pos, vertical_size)
        border_right = pygame.Rect(right_pos, vertical_size)
        border_top = pygame.Rect(top_pos, horizontal_size)
        border_bottom = pygame.Rect(bottom_pos,horizontal_size)

        for border in [border_left,border_right,border_top,border_bottom]:
            pygame.draw.rect(self.surface, color, border)
    
    def add_panel(self) -> None:
        """
        A panel (pygame.Surface) to hold icons that serve as features
        """
        panel_color = (6, 57, 112)
        panel_position = (0,self.SCREEN_HEIGHT)
        self.panel = pygame.Surface((self.SCREEN_WIDTH, self.panel_height))
        self.panel.fill(panel_color)
        icon_count = len(icon_dict)
        icon_width = self.SCREEN_WIDTH / icon_count
        icon_height = self.panel_height
        icon_surface_list = self.get_icon_surfaces(icon_count=icon_count, icon_width=icon_width, icon_height=icon_height)
        x,y=0,0
        
        #attach each image in the icon_dict to icon_surface, and update dict with corresponding rect of icon_surface
        for icon_surface, icon_name in zip(icon_surface_list,icon_dict.keys()):
            img_scaled = pygame.transform.scale(icon_dict[icon_name][0], icon_surface.get_size())
            icon_surface.blit(img_scaled,(0,0))
            self.panel.blit(icon_surface,(x,y))

            #add this rect to icon_dict to map each img position to its surface
            icon_rect = pygame.Rect(x,self.SCREEN_HEIGHT,icon_width, icon_height)
            icon_dict[icon_name].append(icon_rect)

            x += icon_width+2

        self.surface.blit(self.panel, panel_position)
    
    def get_icon_surfaces(self, icon_count:int, icon_width:int, icon_height:int)-> list:
        """
        Add surface on the panel for each icon
        :param icon_count   : the count of icons to be present on the panel
        :param icon_width   : width of each icon that will be placed on panel
        :param icon_height  : height of each icon
        :return (list)      : list of objects(pygame.Surface)
        """
        icon_color = (178,132,190)
        
        icon_surface_list = []
        for _ in range(icon_count):
            icon_surface = pygame.Surface((icon_width, icon_height ))
            icon_surface.fill(icon_color)
            icon_surface_list.append(icon_surface)
        #pygame.draw.rect(icon_surface, icon_color, (0,0,icon_width,icon_height), 2)
        return icon_surface_list

    
    def display_text(self, text:str, position:tuple = None, rel_pos:tuple = None, 
                        color:tuple=None , font_type:'pygame.font'=None) -> None:
        """
        Call this funtion to write a text on the game window
        :param text (str)       : The text to be displayed on the game window
        :param position (tuple) : the (x,y) coordinates where the text will be placed
        :param rel_pos (tuple(int, int))  : relative position on the window for the text
        :param color (tuple)    : rgb value of text
        :param font_type (font) : font of the text
        :return                 : None 
        """
        if position == None:
            if rel_pos == None:
                position = (self.SCREEN_WIDTH/5, self.SCREEN_HEIGHT/4)
            else:
                position = (self.SCREEN_WIDTH/rel_pos[0], self.SCREEN_HEIGHT/rel_pos[1])

        if color == None:
            color = (100,100,100)
        if font_type == None:
            font_type = self.msg_font
        
        label = font_type.render(text, 1, color)
        self.screen.blit(label, position)

    def display_scoreboard(self,score:int, level:int) -> None:
        """
        Display texts to show current score and level
        :param score: the current score of the game
        :param level: the current level of the game
        :return : None
        """
        score_x = self.SCREEN_WIDTH - 100
        y = 10
        score_position = (score_x,y)
        score_text = 'Score : ' + str(score)
        level_x = 10
        level_position = (level_x,y)
        level_text = 'Level : ' + str(level)

        self.display_text(score_text, position=score_position,font_type = self.score_font)
        self.display_text(level_text, position=level_position,font_type = self.score_font)



@dataclass
class UnitCell:
    """
    A single cell (a squre) that can be used both as food and snake's body
    :param x (int)          : x coordinate of the cell
    :param y (int)          : y coordinate of the cell
    :param size (int)       : this will be the side of the square
    :param color (tuple)    : rgb value of the cell
    :return : None
    """
    x:int
    y:int
    size:int
    color:tuple = (0,0,255)

    def __post_init__(self) -> None:
        self.position = [self.x, self.y]
        self.rect = pygame.Rect((self.position ), (self.size*2, self.size*2))
        self.rect.center = (self.position )


class Food(UnitCell):
    """
    Food extends UnitCell and positions on the game window randomly
    """
    def __init__(self,x,y,size = 5,food_color=(255,0,0)) -> None:
        super().__init__(x=x, y=y, size = size, color=food_color)
        self.icon:'an image' = None


@dataclass
class Snake:
    """
    Snake is made up of one or more UnitCell
    :param starting_position (tuple) : (x,y) coordinates for the starting position of the snake
    :param cell_size (int)          : size of each square that the snake is made up of
    :param color (tuple)            : color of snake in rgb
    :return                         : None
    """
    starting_position:tuple
    cell_size:int=5
    color:tuple = (0,0,255)
    body = []
    tail = None
    old_tail = None

    def __post_init__(self) -> None:
        self.cell_gap = self.cell_size*2.2
        self.head = UnitCell(x=self.starting_position[0],
                            y=self.starting_position[1], size=self.cell_size)
        
        self.body.append(self.head) #last cell in body is always head
        log.logger.info(f'Created a snake {self.__dict__}')

    def add_new_cell_to_head(self,cell:UnitCell) -> None:
        """
        Increase the size of the snake by adding cells
        :param cell (UnitCell)  : an instance of UnitCell
        :return                 : None
        """
        new_cell = UnitCell(x=cell.x, y=cell.y, size=self.cell_size)
        self.body.append(new_cell)
        self.update_head()

    def update_head(self) -> None:
        """
        Updates the current head as the newly added UnitCell
        :return : None
        """
        self.head = self.body[-1]


    def move(self, direction:str) -> None:
        """
        Finds (x,y) position of the next UnitCell to be added to the snake
        :param direction (str)  : the direction in which to find the next head
        :return                 : None
        """

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
        new_head = UnitCell(x=new_x, y=new_y,size=self.cell_size)
        self.body.append(new_head)
        self.old_tail = self.body.pop(0)
        self.tail = self.body[0]
        self.update_head()

    def reset(self) -> None:
        """
        reset will destroy body and move the head to starting position
        :return : None
        """
        self.body = []
        self.__post_init__()

