import arcade

BULLET_SCALE = 0.5


class Bullet(arcade.Sprite):
    """
    Bullet class for use with weapons
    """
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

