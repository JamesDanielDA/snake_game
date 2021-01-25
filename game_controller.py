import pygame
import random
import sys
from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass, field
import asyncio
from game_objects import Snake, Food, GameWindow, icon_dict
from icons import backgrounds
from game_rules import GameRules
from logger import GameLogger

log = GameLogger(file_dunder_name = __name__)

@dataclass
class GameController:
    """
    This class controlls the movements of game objects, checks for game rules and follows player commands

    """
    input_queue:list = field(default_factory=list)
    mouse_clicks:list = field(default_factory=list)
    input_listener_delay:float = .01
    mainloop_delay:float = 0.3
    running:bool =True
    food_score:int = 10
    score = {'total':0, 1:0}
    game_level:int = 1
    max_level_score:int = 50
    level_speed_factor:float = 1.0
    next_level_ok:bool = True

    def __post_init__(self) -> None:

        #create main game window
        self.window = GameWindow()
        self.screen = self.window.screen

        #create a snake
        starting_position = (self.window.SCREEN_WIDTH/2, self.window.SCREEN_HEIGHT/2)
        self.snake = Snake(starting_position=starting_position)

        #create random food
        wall_offset = 2
        self.randx = lambda:random.randint(wall_offset, self.window.SCREEN_WIDTH -wall_offset)
        self.randy = lambda:random.randint(wall_offset, self.window.SCREEN_HEIGHT -wall_offset)
        self.food = Food(x=self.randx(), y=self.randy())

        #create gamerules object
        self.gamerules = GameRules(snake=self.snake,
                                    window=self.window)

        self.tkwindow = Tk().wm_withdraw()

        #keybindings for directions
        self.commands = {pygame.K_UP:'up',
                            pygame.K_DOWN:'down',
                            pygame.K_LEFT:'left',
                            pygame.K_RIGHT:'right',
                            pygame.K_SPACE: 'pause'}

        log.logger.info('Game Controller initialized')
    
    def quit_game(self) -> None:
        log.logger.info('Exiting the game')
        pygame.quit()
        sys.exit()

    def should_continue(self, msg:str, testing:bool=False) -> None:
        """
        Once the player loses, call this method to start from beginning
        :param msg : The yes/no question to be shown to the player
        :param testing: unit testing flag
        :returns : None

        """
        
        if not testing:
            continue_game = messagebox.askquestion(title='Continue',message= msg)
        else:
            continue_game = 'yes'
        if continue_game == 'yes':    
            self.snake.reset()
            self.screen.fill(self.window.BG_COLOR)
            self.throw_new_food()
            self.running = True
        else:
            log.logger.info('Player choosed to quit')
            self.quit_game()

    def check_for_rule_violation(self) -> str:
        """
        After each movement of the snake check if any rule is violated
        :returns : str/None
        """
        # check if the snake hit a wall
        if self.gamerules.hit_a_wall():
            rule = 'Snake hit on the Wall!'
            log.logger.info(rule)
            return  rule + '\n\n Do you wish to continue?'

        # check if snake has bitten itself
        if self.gamerules.self_bitten():
            rule = 'Snake has bitten itself!'
            log.logger.info(rule)
            return rule + '\n\n Do you wish to continue?'

        return None


    async def input_handler(self) -> None:
        """
        asynchronous method to listen to keyboard inputs and store it as a list
        :returns : None
        """
        log.logger.info('input_handler started')
        while True:
            
            for event in pygame.event.get():

                #listen to quit request
                if event.type == pygame.QUIT:
                    self.input_queue.append('quit')
                    return
                
                #listen to mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    self.mouse_clicks.append((x,y))

                #listen to keypress events
                if event.type == pygame.KEYDOWN and event.key in self.commands:
                    if event.key == pygame.K_SPACE:
                        if self.paused:
                            self.paused = False
                            log.logger.info('Game Resumed')
                        else:
                            self.paused = True
                            log.logger.info('Game Paused')
                    else:
                        self.input_queue.append(event.key)
            await asyncio.sleep(self.input_listener_delay)
        log.logger.info('input_handler stoped')
        
    
    def throw_new_food(self) -> None:
        """ 
        call this function to throw new food after snake eats the current food
        :returns : None
        """
        self.food = Food(x=self.randx(), y=self.randy())
        pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)
        pygame.display.update()

    def draw_current_food(self) -> None:
        """
        Call this funtion before snake is drawn so that snake will appear on top of food
        :returns : None
        """
        if self.food.icon == None:
            pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)
        else:
            self.window.surface.blit(self.food.icon, self.food.position)

    def enter_next_level(self) -> None:
        """
        Increases snake speed, informs player about the next level
        :returns : None
        """
        continue_game = messagebox.askquestion(title='Next Level',message= f'Well Done! \n\n Enter Level {int(self.game_level+1)}')
        if continue_game == "yes":
            self.mainloop_delay /= self.level_speed_factor * self.game_level
            self.game_level += 1
            self.score[self.game_level] = 0
            self.running = True
        else:
            self.next_level_ok = False
            log.logger.info(f'Player chooses to continue in level {self.game_level}')

    def increment_score(self) -> None:
        """
        Call this function when snake's body adds a cell
        :returns : None
        """
        self.score[self.game_level] += self.food_score
        self.score['total'] += self.food_score

    def select_feature(self,feature):
        if feature in backgrounds:
            self.window.render_background(icon_dict[feature][0])
        
        elif feature in food_icons:
            self.food.icon = icon_dict[feature][0]

    async def mainloop(self) -> None:
        """
        Asychronous function that keeps updating the game window with the latest state
        :returns : None
        """

        
        # Display the initial state of the game
        self.screen.fill(self.window.BG_COLOR)
        self.window.display_text(text='Use arrow keys to change direction of the snake', rel_pos=(5,2))
        self.throw_new_food()
        command = pygame.K_RIGHT #default command
        
        self.paused = True

        while self.running:
            if 'quit' in self.input_queue:
                    self.quit_game()
            
            #check if player has clicked to select a new feature
            for click in self.mouse_clicks:
                for icon_name, img_pair in icon_dict.items():
                    if img_pair[1].collidepoint(click):
                        self.select_feature(feature=icon_name)
                        
                self.mouse_clicks.remove(click)
            
            if self.paused:
                self.window.display_text(text='Game Paused. Press spacebar to resume game.')
                pygame.display.update()
                await asyncio.sleep(self.mainloop_delay*2)
            
            else:
                #clear previous screen
                self.screen.fill(self.window.BG_COLOR)

                # check for player's next command in the input_queue
                try:
                    command = self.input_queue.pop(0)
                except IndexError:
                    pass

                # move snake in the direction of player's command
                direction = self.commands[command]
                self.snake.move(direction)

                #draw game objects on the screen
                self.screen.blit(self.window.surface,(0,0))
                self.window.display_scoreboard(score=self.score['total'], level=self.game_level)
                self.draw_current_food()
                for cell in self.snake.body:
                    pygame.draw.rect(self.screen, cell.color, cell.rect)
                
                #Check if snake has eaten
                eaten_food = self.gamerules.eaten_food(self.food)
                if eaten_food:
                    self.snake.add_new_cell_to_head(eaten_food)
                    self.increment_score()
                    self.throw_new_food()
                self.window.display_scoreboard(score=self.score['total'], level=self.game_level)
                
                pygame.display.update()

                # After this move, check if all the rules have been met
                violation = self.check_for_rule_violation()
                if violation != None:
                    log.logger.info('hit on wall at ',self.snake.head.position)
                    self.should_continue(msg=violation)

                #check if current level is completed, if player wants to go to next level
                if self.next_level_ok:
                    if self.gamerules.check_level_completed(score=self.score[self.game_level], 
                                                        max_level_score=self.max_level_score):
                        self.enter_next_level()

                await asyncio.sleep(self.mainloop_delay)
