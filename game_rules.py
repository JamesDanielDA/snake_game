#game rules are defined and checked  in this module

from dataclasses import dataclass
from math import hypot

@dataclass
class GameRules:
    snake:object
    window:object

    def __post_init__(self):
        self.boundaries = {"left"   : 0 + self.snake.cell_size,
                            "right" : self.window.SCREEN_WIDTH - self.snake.cell_size,
                            "up"    : 0 + self.snake.cell_size,
                            "down"  : self.window.SCREEN_HEIGHT - self.snake.cell_size}
    
    def hit_a_wall(self):
        """
        Check if snake's head has hit any of the four walls
        """
        snake = self.snake
        if snake.moving_direction == "left" and snake.head.x <= self.boundaries["left"]:
            return True
        if snake.moving_direction == "right" and snake.head.x >= self.boundaries["right"]:
            return True
        if snake.moving_direction == "up" and snake.head.y <= self.boundaries["up"]:
            return True
        if snake.moving_direction == "down" and snake.head.y >= self.boundaries["down"]:
            return True

        return False

    def self_bitten__(self):
        """
        check if the head has come close enough to any of its body cells
        """
        safe_length = 4
        if len(self.snake.body) <= safe_length:
            return False

        for cell in self.snake.body[0: len(self.snake.body)- safe_length]:
            bite_distance = hypot(self.snake.head.x - cell.x,  self.snake.head.y - cell.y)
            if bite_distance <= self.snake.cell_gap:
                return True

    def self_bitten(self):
        """
        check if the head has come close enough to any of its body cells
        """
        safe_length = 4
        head = self.snake.head
        if len(self.snake.body) > safe_length:
            for cell in self.snake.body[0:len(self.snake.body)- safe_length]:
                if head.rect.colliderect(cell.rect):
                    return True
        return False

    def eaten_food(self,food):
        """
        check if head of snake collides with food
        """
        head = self.snake.head
        if head.rect.colliderect(food.rect):
            return food
        return None

