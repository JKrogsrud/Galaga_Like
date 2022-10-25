import arcade
from weapon import Weapon
import math

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class Enemy(arcade.Sprite):
    def __init__(self,
                 filename,
                 destination=0,
                 position_in_battle_line=0,
                 scale=0.375,
                 weapon=Weapon(),
                 hp=1,
                 time_between_firing=2.0,
                 speed_to_formation=10,
                 speed_in_formation=2
                 ):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.weapon = weapon
        self.weapon.friendly = False
        self.time_since_last_firing = 0
        self.time_between_firing = time_between_firing
        self.to_fire = False
        self.in_formation = False
        self.destination = destination
        self.position_in_battle_line = position_in_battle_line
        self.speed_to_formation = speed_to_formation
        self.speed_in_formation = speed_in_formation
        self.moving_right = True

    def update(self, delta_time: float = 1 / 60):
        if not self.in_formation:
            # Move to destination in the battle line
            # First we do some math..
            delta_x = self.destination[0] - self.center_x
            delta_y = self.destination[1] - self.center_y
            dist = math.sqrt(delta_x**2 + delta_y**2)
            if dist < 5:
                self.center_x = self.destination[0]
                self.center_y = self.destination[1]
                self.in_formation = True
            else:
                change_x = (delta_x * self.speed_to_formation) / dist
                change_y = (delta_y * self.speed_to_formation) / dist

                self.center_x += change_x
                self.center_y += change_y
        else:
            # Should move back and forth at a speed consistent with the battle line
            if self.moving_right:
                self.center_x += self.speed_in_formation
            else:
                self.center_x -= self.speed_in_formation

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
