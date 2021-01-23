import pygame
import random
from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass, field
import asyncio
from game_objects import Snake, Food, GameWindow
from game_rules import GameRules
from logger import GameLogger

log = GameLogger(file_dunder_name = __name__)

@dataclass
class GameController:
    """
    This class controlls the movements of game objects, checks for game rules and follows player commands
    """
    input_queue:list = field(default_factory=list)
    input_listener_delay:float = .01
    mainloop_delay:float = 0.3
    running:bool =True
    food_score:int = 10
    current_level_score:int = 0
    prev_level_score:int = 0
    total_score:int = 0
    game_level:int = 1
    max_level_score:int = 10
    level_speed_factor:float = 1.0

    def __post_init__(self) -> None:

        #create game window
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

    def quit_game(self) -> None:
        log.logger.info('Exiting the game')
        pygame.quit()
        sys.exit()

    def should_continue(self, msg:str, testing:bool=False) -> None:
        """
        Once the player loses, call this method to start from beginning
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
            self.quit_game()

    def check_for_rule_violation(self) -> str:
        """
        After each movement of the snake check if any rule is violated
        """
        # check if the snake hit a wall
        if self.gamerules.hit_a_wall():
            return "Snake hit on the Wall! \n\n Do you wish to continue?"

        # check if snake has bitten itself
        if self.gamerules.self_bitten():
            return "Snake has bitten itself!  \n\n Do you wish to continue?"

        return None


    async def input_handler(self) -> None:
        """
        asynchronous method to listen to keyboard inputs and store it as a list

        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.input_queue.append('quit')
                    return
                
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
    
    def throw_new_food(self) -> None:
        """ 
        call this function to throw new food after snake eats the current food
        """
        self.food = Food(x=self.randx(), y=self.randy())
        pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)
        pygame.display.update()

    def draw_current_food(self) -> None:
        """
        Call this funtion before snake is drawn so that snake will appear on top of food
        """
        pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)

    def enter_next_level(self) -> None:
        """
        Should only be called when a game_leve is completed ie. score == multiples of max_level_score
        Determines whther to move to the next level and decreases the delay time of the mainloop accordingly
        :param score: the current score
        :return: None if player doesn't want to go to next level
        """
        self.mainloop_delay /= self.level_speed_factor * self.game_level
        continue_game = messagebox.askquestion(title='Next Level',message= f'Well Done! \n\n Enter Level {int(self.game_level+1)}')
        if continue_game == "yes":
            self.game_level += 1
            self.prev_level_score += self.current_level_score
            self.current_level_score = 0    
            #self.snake.reset()
            #self.throw_new_food()
            self.window.display_scoreboard(self.total_score, self.game_level)
            self.running = True
        else:
            self.should_continue(msg = "Continue current level?")

    def calculate_score(self) -> None:
        """
        Call this function when snake's body size increases
        """
        self.current_level_score = (len(self.snake.body)-1)*self.food_score
        self.total_score = self.current_level_score + self.prev_level_score

    async def mainloop(self) -> None:
        
        # Display the initial state of the game
        self.screen.fill(self.window.BG_COLOR)
        self.throw_new_food()
        command = pygame.K_RIGHT #default command
        
        self.paused = False

        while self.running:
            if 'quit' in self.input_queue:
                    self.quit_game()
            
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
                
                # #calculate scores
                # self.current_level_score = (len(self.snake.body)-1)*self.food_score
                # self.total_score = self.prev_level_score + self.current_level_score
                # self.window.display_scoreboard(score=self.total_score, level=self.game_level)

                #draw game objects on the screen
                self.window.display_scoreboard(score=self.total_score, level=self.game_level)
                self.draw_current_food()
                for cell in self.snake.body:
                    pygame.draw.rect(self.screen, cell.color, cell.rect)
                
                #Check if snake has eaten
                eaten_food = self.gamerules.eaten_food(self.food)
                if eaten_food:
                    self.snake.add_new_cell_to_head(eaten_food)
                    self.calculate_score()
                    self.throw_new_food()
                self.window.display_scoreboard(score=self.total_score, level=self.game_level)
                
                pygame.display.update()

                # After this move, check if all the rules have been met
                violation = self.check_for_rule_violation()
                if violation != None:
                    self.should_continue(msg=violation)

                #check if current level is completed
                if self.gamerules.check_level_completed(score=self.current_level_score, 
                                                    max_level_score=self.max_level_score):
                    self.enter_next_level()

                await asyncio.sleep(self.mainloop_delay)
