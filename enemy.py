import arcade
from weapon import Weapon

class Enemy(arcade.Sprite):
    def __init__(self, filename="Enemy_1.png", weapon=Weapon(), hp=1):
        super().__init__(filename=filename)
        self.hp = hp
        self.weapon = weapon

    # Probably need to change this
    def update(self):
        # Check for out-of-bounds
        if self.left < 10:
            self.change_x = 5
        elif self.right > SCREEN_WIDTH - 10:
            self.change_x = -5