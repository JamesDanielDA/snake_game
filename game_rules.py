#game rules are defined and checked  in this module

from dataclasses import dataclass
from math import hypot

@dataclass
class GameRules:
    snake:object
    window:object

    def __post_init__(self):
        self.boundaries = {"left"   : 0 + self.snake.cell_size*2,
                            "right" : self.window.SCREEN_WIDTH - self.snake.cell_size*2,
                            "up"    : 0 + self.snake.cell_size*2,
                            "down"  : self.window.SCREEN_HEIGHT - self.snake.cell_size*2}
    
    def hit_a_wall(self):
        """
        Check if snake's head has hit any of the four walls
        """
        snake = self.snake
        if snake.moving_direction == "left" and snake.head.x < self.boundaries["left"]:
            return True
        if snake.moving_direction == "right" and snake.head.x > self.boundaries["right"]:
            return True
        if snake.moving_direction == "up" and snake.head.y < self.boundaries["up"]:
            return True
        if snake.moving_direction == "down" and snake.head.y > self.boundaries["down"]:
            return True

        return False

    def self_bitten(self):
        """
        check if the head has touched snake's own body
        """
        pass

    def eaten_food(self,food):
        """
        check if head touched the food
        """
        snake = self.snake
        #find the distance btw snake's head center and center of food
        distance = hypot(snake.head.x-food.x, snake.head.y-food.y)
        if distance < (food.size + snake.cell_size):
            print('head touched food')
            return food
        return False

