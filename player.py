import arcade
from weapon import Weapon
from bullet import Bullet

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

class Player(arcade.Sprite):
    def __init__(self, filename="Player.png",
                 lives=3,
                 weapon=Weapon(),
                 movement_speed=10):
        super().__init__(filename, scale=0.035)
        self.lives = lives
        self.weapon = weapon
        self.movement_speed = movement_speed
        self.left_pressed = False
        self.right_pressed = False

    def update(self):
        """ Move the player """
        # Move player.
        self.center_x += self.change_x

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

    # Creates a bullet that the weapon should create
    def fire(self):
        bullet = self.weapon.fire(self.center_x, self.bottom + self.height)
        return bullet

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.change_x = -self.movement_speed
        elif self.right_pressed and not self.left_pressed:
            self.change_x = self.movement_speed

