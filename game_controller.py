import pygame
import random
from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass, field
import asyncio
from game_objects import Snake, Food, GameWindow
from game_rules import GameRules


@dataclass
class GameController:
    """
    This class controlls the movements of game objects, checks for game rules and follows player commands
    """
    input_queue:list = field(default_factory=list)
    input_listener_delay:float = .01
    mainloop_delay:float = .3
    running:bool = True

    def __post_init__(self):

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
        #self.food = Food(x=self.randx(), y=self.randy())

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

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def should_continue(self, msg):
        """
        Once the player loses, call this method to start from beginning
        """
        continue_game = messagebox.askquestion(title='Continue',message=f'{msg} \n\nDo you wish to restart')
        if continue_game == "yes":    
            self.snake.reset()
            self.screen.fill(self.window.BG_COLOR)
            self.throw_new_food()
            self.window.display_score(0)
            self.running = True
        else:
            self.quit_game()

    def check_for_rule_violation(self):
        """
        After each movement of the snake check if any rule is violated
        """
        # check if the snake hit a wall
        if self.gamerules.hit_a_wall():
            return "Snake hit on the Wall!"

        # check if snake has bitten itself
        if self.gamerules.self_bitten():
            return "Snake has bitten itself!"

        return None


    async def input_handler(self):
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
                        self.paused = True if self.paused == False else False
                    else:
                        self.input_queue.append(event.key)
            await asyncio.sleep(self.input_listener_delay)

    def throw_new_food(self):
        """ 
        call this function to throw new food after snake eats the current food
        """
        self.food = Food(x=self.randx(), y=self.randy())
        pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)
        pygame.display.update()

    def draw_current_food(self):
        """
        Call this funtion before snake is drawn so that snake will appear on top of food
        """
        pygame.draw.circle(self.screen, self.food.color, self.food.position, self.food.size)

    async def mainloop(self):
        
        # Display the initial state of the game
        self.screen.fill(self.window.BG_COLOR)
        self.throw_new_food()
        command = pygame.K_RIGHT #default command
        
        self.paused = False
        while self.running:
            if 'quit' in self.input_queue:
                    self.quit_game()
            
            if self.paused:
                self.window.display_text('Game Paused. \n\nPress spacebar to resume game.')
                await asyncio.sleep(self.mainloop_delay)
            
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
                
                #draw all the current cells of snake's body and food
                score = (len(self.snake.body)-1)*10
                self.window.display_score(score)
                self.draw_current_food()
                for cell in self.snake.body:
                    pygame.draw.rect(self.screen, cell.color, cell.rect)
                pygame.display.update()

                # After this move, check if all the rules have been met
                violation = self.check_for_rule_violation()
                if violation != None:
                    self.should_continue(msg=violation)
                    

                #Check if snake has eaten
                eaten_food = self.gamerules.eaten_food(self.food)
                if eaten_food:
                    self.snake.add_new_cell_to_head(eaten_food)
                    self.throw_new_food()

                self.window.display_score(score)
                await asyncio.sleep(self.mainloop_delay)
