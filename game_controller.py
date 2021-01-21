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
    This class is the brain of the game that coordinates between game objects and player
    """
    input_queue:list = field(default_factory=list)
    input_listener_delay:float = .01
    mainloop_delay:float = .05
    running:bool = True

    def __post_init__(self):

        #create game window
        self.window = GameWindow()
        self.screen = self.window.screen

        #create a snake
        starting_position = (self.window.SCREEN_WIDTH/2, self.window.SCREEN_HEIGHT/2)
        self.snake = Snake(starting_position=starting_position)

        #create random food
        self.randx = lambda:random.randint(0, self.window.SCREEN_WIDTH)
        self.randy = lambda:random.randint(0, self.window.SCREEN_HEIGHT)
        self.food = Food(x=self.randx(), y=self.randy())

        #create gamerules object
        self.gamerules = GameRules(snake=self.snake,
                                    food=self.food,
                                    window=self.window)

        self.tkwindow = Tk().wm_withdraw()

        #keybindings for directions
        self.commands = {pygame.K_UP:'up', pygame.K_DOWN:'down', pygame.K_LEFT:'left', pygame.K_RIGHT:'right'}

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def should_continue(self, msg):
        """
        Once the player loses, call this method to start from beginning
        """
        continue_game = messagebox.askquestion(title='Continue',message=f'{msg} \n\nDo you wish to continue')
        if continue_game == "yes":    
            self.snake.reset()
            self.screen.fill(self.window.BG_COLOR)
            self.running = True
        else:
            self.quit_game()


    def check_for_rule_violation(self):
        """
        After each move of snake check if any of the rules is violated
        """
        # check if the snake hit a wall
        if self.gamerules.hit_a_wall():
            return "Snake hit on the Wall!"

        return None
            

    async def input_listener(self):
        """
        asynchronous method to listen to keyboard inputs and store it in as a list
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.input_queue.append('quit')
                    return
                if event.type == pygame.KEYDOWN:
                    self.input_queue.append(event.key)
                    print(f'commands pending - {self.input_queue}')
            await asyncio.sleep(self.input_listener_delay)

    async def mainloop(self):
        
        # Fill the background with white
        self.screen.fill(self.window.BG_COLOR)
        command = pygame.K_RIGHT #default command

        while self.running:
            if 'quit' in self.input_queue:
                self.quit_game()

            # check for player's next command in the input_queue
            try:
                command = self.input_queue.pop(0)
            except IndexError:
                pass

            # move snake in the direction of player's command
            direction = self.commands[command]
            self.snake.move(direction)

            #remove old tail from screen
            tail = self.snake.old_tail
            pygame.draw.circle(self.screen, self.window.BG_COLOR, tail.position, tail.size)
            
            #draw all the current cells of snake's body
            for cell in self.snake.body:
                pygame.draw.circle(self.screen, cell.color, cell.position, cell.size)
            
            #throw a random food on the screen
            food = Food(x=self.randx(), y=self.randy())
            #pygame.draw.circle(self.screen, food.color, food.position, food.size)
            pygame.display.update()

            # After this move, check if all the rules have been met
            violation = self.check_for_rule_violation()
            if violation != None:
                self.should_continue(msg=violation)


            await asyncio.sleep(self.mainloop_delay)
