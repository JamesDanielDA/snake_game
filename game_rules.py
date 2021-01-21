#game rules are defined and checked  in this module

from dataclasses import dataclass

@dataclass
class GameRules:
    snake:object
    food:object
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
        food = self.food
        if snake.moving_direction == "left" and snake.head.x_cord < self.boundaries["left"]:
            return True
        if snake.moving_direction == "right" and snake.head.x_cord > self.boundaries["right"]:
            return True
        if snake.moving_direction == "up" and snake.head.y_cord < self.boundaries["up"]:
            return True
        if snake.moving_direction == "down" and snake.head.y_cord > self.boundaries["down"]:
            return True

        return False

    def self_bitten(self):
        """
        check if the head has touched snake's own body
        """
        pass

    def eaten_food(self):
        """
        check if head touched the food
        """
        pass

