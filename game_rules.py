#game rules are defined and checked  in this module

from dataclasses import dataclass
from math import hypot
from logger import GameLogger


#log = GameLogger(file_dunder_name=__name__)

@dataclass
class GameRules:
    """
    A class that detemines if the rules the player/snake has met the rules of the game
    :param snake (Snake)    : the snake object created for the game
    :param window (GameWindow) : the instance of GameWindow
    :return : None
    """

    snake:object
    window:object

    def __post_init__(self) -> None:
        hit_offset = self.snake.cell_size + 1
        self.boundaries = {"left"   : 0 + hit_offset,
                            "right" : self.window.SCREEN_WIDTH - hit_offset,
                            "up"    : 0 + hit_offset,
                            "down"  : self.window.SCREEN_HEIGHT - hit_offset}
    
    def hit_a_wall(self) -> bool:
        """
        Check if snake's head has hit any of the four walls
        :return (bool)
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

    def self_bitten(self) -> bool:
        """
        check if the head has come close enough to any of its body cells
        :return (bool)
        """

        safe_length = 4
        head = self.snake.head
        if len(self.snake.body) > safe_length:
            for cell in self.snake.body[0:len(self.snake.body)- safe_length]:
                if head.rect.colliderect(cell.rect):
                    return True
        return False

    def eaten_food(self,food:object) -> object:
        """
        check if head of snake collides with food
        :param food (Food)  : the Food object
        :return (Food)      : None/Food
        """
        head = self.snake.head
        if head.rect.colliderect(food.rect):
            return food
        return None

    def check_level_completed(self,score:int, max_level_score:int) -> bool:
        """
        checks if a level is completed by comparing score against max_level_score
        :param score (int)          : the current score
        :param max_level_score(int)  : max score allowed in the level
        :return (bool) 
        """
        return score == max_level_score:


