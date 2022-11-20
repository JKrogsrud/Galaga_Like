from bullet import Bullet
import copy
import math

"""
Weapon class will handle the starting position and types of bullets
that will be used in the game.

:param image:  the image file used for the weapon if it has one (unused but would be implemented with weapon powerups)
:param friendly: a boolean as to whether or not the bullets fired from this weapon harm the player
:param requires_ammo: a boolean as to whether or not the weapon requires ammunition to fire
:param ammo: The amount of ammo in the gun
:param bullet_type: Bullet class fired by this weapon
:param bullet-speed: the speed of the bullets that are fired
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
