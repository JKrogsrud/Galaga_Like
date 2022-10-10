import arcade


class Bullet(arcade.Sprite):
    """
    Bullet class for use with weapons
    """
    def __init__(self, filename= "blue_lazer.png", center_y=0, center_x=0, damage=1):
        super().__init__(filename=filename, center_x=center_x, center_y=center_y)
        self.damage = damage

    def update_trajectory(self):
        # Code here for how different types of bullets may change over time
        pass