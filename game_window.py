import pygame
from snake import Snake
from tkinter import *
from tkinter import messagebox

#from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

pygame.init()

# Set up the drawing window
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
HEAD_SIZE = 5
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Run until the user asks to quit

running = True
starting_pos = (250, 250)

snake = Snake(starting_pos=starting_pos,width=SCREEN_WIDTH , height=SCREEN_HEIGHT, head_size=HEAD_SIZE)
Tk().wm_withdraw() #to hide the main window

def restart_game():
    global running
    continue_game = messagebox.askquestion(title='Continue',message='Snake Hit!! \n\nDo you want to continue')
    if continue_game == "yes":    
        print("Restarting Game")
        snake.restart()
        running = True
        main()


def main():
    global running
    while running:
        pygame.time.delay(50)
        if snake.has_collided:
            print(f"Collided, now at  {snake.head_position}")
            running = False
            restart_game()
        # Did the user click the window close button?

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill((255, 255, 255))

        # move snake in the directions
        snake.move("up")
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 255), snake.head_position, HEAD_SIZE)
        pygame.display.update()
        
main()
pygame.quit()