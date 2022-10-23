import arcade
from weapon import Weapon

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class Enemy(arcade.Sprite):
    def __init__(self, filename="Enemy_1.png", scale=0.375, weapon=Weapon(), hp=1, time_between_firing=2.0):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.weapon = weapon
        self.weapon.friendly = False
        self.time_since_last_firing = 0
        self.time_between_firing = time_between_firing
        self.to_fire = False

    def update(self, delta_time: float = 1 / 60):
        # Check for out-of-bounds
        if self.left < 10:
            self.change_x = 5
        elif self.right > SCREEN_WIDTH - 10:
            self.change_x = -5

        # Check if the enemy has fired recently
        self.time_since_last_firing += delta_time

        # Check this value against time_between_firing
        if self.time_since_last_firing >= self.time_between_firing:

            # Reset firing timer
            self.time_since_last_firing = 0

            # Set need to fire as True
            self.to_fire = True

    def fire(self):
        self.to_fire = False
        bullet = self.weapon.fire(self.center_x, self.top - self.height)
        return bullet
