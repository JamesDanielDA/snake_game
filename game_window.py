import pygame
from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass
import logging
from snake import Snake

#setting up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s:%(messages)s")

file_handler = logging.FileHandler("game_window.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

#from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

pygame.init()

@dataclass
class GameWindow:
    """
    Create an object of this class to put a snake
    The look and feel of the game is decided by this class
    """
    
    SCREEN_WIDTH:int = 500
    SCREEN_HEIGHT:int = 500
    HEAD_SIZE:int = 5
    running = True
    starting_head_position = (250, 250)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    def __post_init__(self):
        #create a snake with respect to  the GameWindow object
        self.snake = Snake(starting_position=self.starting_head_position,
                        width=self.SCREEN_WIDTH , 
                        height=self.SCREEN_HEIGHT, 
                        head_size=self.HEAD_SIZE)
        #create and hide a tkinter window to display messages
        self.tkwindow = Tk().wm_withdraw() 

    def reset_game(self):
        """
        Once the player loses, call this method to reset the snake
        """
        continue_game = messagebox.askquestion(title='Continue',message='Snake Hit! \n\nDo you want to continue')
        if continue_game == "yes":    
            logger.info("Restarting Game")
            self.snake.reset()
            self.running = True
            self.mainloop()


    def mainloop(self):
        while self.running:
            pygame.time.delay(50)
            if self.snake.has_collided:
                logger.info(f"Snake Collided  at  {self.snake.head_position}")
                self.running = False
                self.reset_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill the background with white
            self.screen.fill((255, 255, 255))

            # move snake in the directions
            self.snake.move("up")
            self.screen.fill((255, 255, 255))
            pygame.draw.circle(self.screen, (0, 0, 255), self.snake.head_position, self.HEAD_SIZE)
            pygame.display.update()

        self.tkwindow.destroy()
        pygame.quit()
        sys.exit()

