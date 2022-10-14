import arcade
from weapon import Weapon
from bullet import Bullet

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

class Player(arcade.Sprite):
    def __init__(self, filename=":resources:images/space_shooter/playerShip1_blue.png", lives=3, weapon=Weapon()):
        super().__init__(filename, scale=0.5)
        self.lives = lives
        self.weapon = weapon

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

    # Creates a bullet that the weapon should create
    def fire(self):

