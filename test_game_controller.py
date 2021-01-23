import unittest
import pygame
from game_controller import GameController

class TestGameController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.game = GameController()
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_GameWindow(self):
        self.assertEqual(pygame.display.get_surface().get_size(),(500,500))
        self.assertEqual(pygame.display.get_caption()[0], 'Snake Game')

    def test_snake_eaten_food(self):
        game = GameController()
        game.snake.add_new_cell_to_head(game.food)
        self.assertEqual(len(game.snake.body), 2)  



if __name__ == "__main__":
    unittest.main()
