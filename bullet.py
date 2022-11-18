import arcade

BULLET_SCALE = 0.5

"""
Bullet class for the projectiles of the game. A child class of the Sprite Class
:param filename: the image file used for visually representing the bullet
:param center_y: the y_coord center of the image
:param center_x: the x_coord center of the image
:param damage: how much damage cause by the bullet
:param speed: how fast the bullet travels after being shot
:param friendly: whether or not the bullet harms the player
:param scale: how much we scale the bullet image by to fit our window
"""
class Bullet(arcade.Sprite):
    def __init__(self, filename="blue_laser.png",
                 center_y=0,
                 center_x=0,
                 damage=1,
                 speed=10,
                 friendly=True,
                 scale=BULLET_SCALE):
        super().__init__(filename=filename, center_x=center_x, center_y=center_y, scale=scale)
        self.damage = damage
        self.speed = speed
        self.friendly = friendly

    def update(self, delta_time: float = 1 / 60):
        if self.friendly:
            self.center_y += self.speed
        else:
            self.center_y -= self.speed

