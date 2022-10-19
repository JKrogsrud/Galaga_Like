import arcade
from weapon import Weapon

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

class Enemy(arcade.Sprite):
    def __init__(self, filename="Enemy_1.png", scale=0.375, weapon=Weapon(), hp=1):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.weapon = weapon

    # Probably need to change this
    def update(self):
        # Check for out-of-bounds
        if self.left < 10:
            self.change_x = 5
        elif self.right > SCREEN_WIDTH - 10:
            self.change_x = -5

    # def fire()