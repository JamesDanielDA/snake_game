from dataclasses import dataclass, field
from time import sleep

class Snake:
    """
    Object of class Snake can be created and put on a pygame window
    Snake will keep a record of its own body parts in relationship with window coordinates
    pygame captures keystrokes from the player and passes it to Snake which in turn decides all the manouvers 
    """
    def __init__(self, starting_pos:tuple,width:int ,height:int ,head_size:int):
        self.starting_pos = starting_pos
        self.head_x = self.starting_pos[0]
        self.head_y = self.starting_pos[1]
        self.head_position = [self.head_x,self.head_y]
        self.head_direction = None
        self.velocity = 5
        #define boundaries and collision positions
        self.boundaries = {"left":  0 + head_size*2,
                            "right": width - head_size*2,
                            "up":   0 + head_size*2,
                            "down":height - head_size*2}
        #self.refresh_rate= 0.1 #time to sleep before each update of snake positions
        self.has_collided = False

    def move(self, direction):
        """move in the given direction if there is no collision"""
        self.check_collision()
        if self.has_collided:
            print(f"Snake hit a boundary {self.head_position}, you lost!!")
            return
        self.head_direction = direction
        # find the new coordinates of  the head according to the direction
        if direction == "left":
            self.head_x -= self.velocity
        if direction == "right":
            self.head_x += self.velocity
        if direction == "up":
            self.head_y -= self.velocity
        if direction == "down":
            self.head_y += self.velocity
        #update the head position with new coordinates
        self.head_position = [self.head_x,self.head_y]
        print("head position at ", self.head_position)

    def check_collision(self):
        #check the direction of head moving and determine if collided with any boundary
        if self.head_direction == "left" and self.head_x < self.boundaries["left"]:
            self.has_collided = True
        if self.head_direction == "right" and self.head_x > self.boundaries["right"]:
            self.has_collided = True
        if self.head_direction == "up" and self.head_y < self.boundaries["up"]:
            self.has_collided = True
        if self.head_direction == "down" and self.head_y > self.boundaries["down"]:
            self.has_collided = True

    def restart(self):
        """
        restart will destroy body and move the head to starting position
        """
        self.head_x = self.starting_pos[0]
        self.head_y = self.starting_pos[1]
        self.has_collided = False
        print(f'restarted snake , has_collided is {self.has_collided}')


