from bullet import Bullet
import copy
import math

"""
Weapon class will handle the starting position and types of bullets
that will be used in the game.

It should know where the player / enemy sprite is so pass in those locations
"""


class Weapon():
    def __init__(self, image=None,
                 friendly=True,
                 requires_ammo=False,
                 ammo=100,
                 bullet_type=Bullet(),
                 bullet_speed=10):
        self.image = image
        self.friendly = friendly
        self.requires_ammo = requires_ammo
        self.ammo = ammo
        self.bullet_type = bullet_type
        self.bullet_speed = bullet_speed

    def fire(self, x_loc, y_loc):
        # Create Bullet object
        if self.ammo > 0 or not self.requires_ammo:  # Ammo available or not needed
            bullet = self.bullet_type
            bullet.friendly = self.friendly
            bullet.center_x = x_loc
            bullet.center_y = y_loc
            bullet.speed = self.bullet_speed

            if self.requires_ammo:  # If ammo required subtract 1 from ammo
                self.ammo -= 1
        else:
            bullet = Bullet(center_x=x_loc, center_y=y_loc)  # Fires basic weapon
            bullet.speed = self.bullet_speed

        # Set the correct orientation
        if not self.friendly:
            bullet.angle = math.radians(math.pi)

        return copy.deepcopy(bullet)
