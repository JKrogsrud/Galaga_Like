from bullet import Bullet

"""
Weapon class will handle the starting position and types of bullets
that will be used in the game.

It should know where the player / enemy sprite is so pass in those lcoations
"""


class Weapon():
    def __init__(self, image, player_loc=(0, 0), requires_ammo=False, ammo=100, bullet_type=Bullet()):
        self.image = image
        self.x_loc = player_loc[0]
        self.y_loc = player_loc[1]
        self.requires_ammo = requires_ammo
        self.ammo = ammo
        self.bullet_type = bullet_type


    def fire(self):
        # Create Bullet object
        if self.ammo > 0 or not self.requires_ammo:  # Ammo available or not needed
            bullet = self.bullet_type
            if self.requires_ammo:  # If ammo required subtract 1 from ammo
                self.ammo -= 1
        else:
            bullet = Bullet(center_x=self.x_loc, center_y=self.y_loc)  # Fires basic weapon
        return bullet