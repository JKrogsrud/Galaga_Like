import arcade
import enemy

SCREEN_WIDTH = 500

# This class represents a moving formation that moves side to side
class Horizontal_Battle_Line(arcade.SpriteList):
    def __init__(self, left_pos, right_pos, speed=10, add_rate=1, num_ships=6, depth=100):
        super().__init__()
        self.positions = []
        self.left_pos = left_pos
        self.right_pos = right_pos
        self.full = False
        self.speed = speed
        self.depth = depth
        self.going_right = True
        self.change_x = speed
        self.moving_forward = False



        # Fill the position tracker with False to imply no ships have been added
        # Each position should be a tuple: ((x_loc,y_loc), boolean is_filled)
        line_width = right_pos - left_pos
        space_between_enemies = line_width / num_ships
        enemy_pos = left_pos
        for index in range(num_ships):
            self.positions.append([[enemy_pos, self.depth], False])
            enemy_pos += space_between_enemies

    def add_enemy(self, position, enemy):
        enemy.speed_in_formation = self.speed
        super().append(enemy)
        enemy.destination = self.positions[position][0]
        enemy.position_in_battle_line = position


    def update(self, delta_time: float = 1 / 60):
        # Update the positions of each enemy inside the formation

        if self.right_pos > SCREEN_WIDTH - 10 and self.going_right:
            self.change_x = -self.speed
            self.going_right = False

        elif self.left_pos < 10 and not self.going_right:
            #  should start moving right
            self.change_x = self.speed
            self.going_right = True

        # Update positions
        for pos in self.positions:
            pos[0][0] += self.change_x

        self.left_pos += self.change_x
        self.right_pos += self.change_x

        # update the destinations for enemy ships
        for enemy in self.sprite_list:
            if not enemy.in_formation:
                enemy.destination = self.positions[enemy.position_in_battle_line][0]
            else:
                enemy.moving_right = self.going_right

        super().update()
