from bullet import Bullet

"""
Weapon class will handle the starting position and types of bullets
that will be used in the game.

It should know where the player / enemy sprite is so pass in those lcoations
"""


class Weapon():
    def __init__(self, image, friendly=True, requires_ammo=False, ammo=100, bullet_type=Bullet()):
        self.image = image
        self.requires_ammo = requires_ammo
        self.ammo = ammo
        self.bullet_type = bullet_type


    def fire(self, x_loc, y_loc):
        # Create Bullet object
        if self.ammo > 0 or not self.requires_ammo:  # Ammo available or not needed
            bullet = self.bullet_type
            bullet.center_x = x_loc
            bullet.center_y = y_loc

            # Set velocity of the of the bullet and set the correct orientation of image

            if self.requires_ammo:  # If ammo required subtract 1 from ammo
                self.ammo -= 1
        else:
            bullet = Bullet(center_x=x_loc, center_y=y_loc)  # Fires basic weapon
        return bullet
