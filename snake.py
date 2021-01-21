from dataclasses import dataclass, field
from time import sleep

@dataclass
class Snake:
    """
    Object of class Snake can be created and put on a pygame window
    Snake will keep a record of its own body parts in relationship with window coordinates
    pygame captures keystrokes from the player and passes it to Snake which in turn decides all the manouvers 
    """
    starting_position:tuple
    width:int
    height:int
    head_size:int
    head_direction:str = 'right'
    velocity:int=5
    has_collided:bool=False
    

    def __post_init__(self):
        self.head_x = self.starting_position[0]
        self.head_y = self.starting_position[1]
        self.head_position = [self.head_x,self.head_y]
        #define all four boundaries relative to the center coordinates of sneak's head
        self.boundaries = {"left"   : 0 + self.head_size*2,
                            "right" : self.width - self.head_size*2,
                            "up"    : 0 + self.head_size*2,
                            "down"  : self.height - self.head_size*2}

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

    def reset(self):
        """
        reset will destroy body and move the head to starting position
        """
        self.head_x = self.starting_position[0]
        self.head_y = self.starting_position[1]
        self.has_collided = False


