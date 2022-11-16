import arcade
import enemy
import math

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
        enemy.battle_line_destination = self.positions[position][0]
        enemy.position_in_battle_line = position

    def update(self, delta_time: float = 1 / 60):
        # Update the positions of each enemy inside the formation

        if self.right_pos > SCREEN_WIDTH+20 and self.going_right:
            self.change_x = -self.speed
            self.going_right = False

        elif self.left_pos < 20 and not self.going_right:
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
            if enemy.move_state == 'charging' and enemy.charge_destination == None:
                enemy.charge_destination = (enemy.center_x, -100)
            elif len(enemy.destination_list) == 1:
                enemy.destination_list.append(self.positions[enemy.position_in_battle_line][0])
            elif enemy.move_state == 'in_formation':
                enemy.moving_right = self.going_right

        super().update()

"""
Create a list of destination points for enemies to use for traversal
These curves are a series of destinations and the ships may or may not follow
them exactly. It's more of a quick fix to get some curved trajectories
-entrance_loc is where (off_screen) the ships will begin
-turn_point is the location of the vertex of the parabola
-num_points is how many sub-destinations will be created for the destination list
-break_point is an x-value that determines the end of the list (when the ship should join a formation)
"""
def parabolic_destination(entrance_loc, turn_point, num_points, break_point):
    if entrance_loc[0] == turn_point[0]:
        # This is a vertical line and math doesn't work the same way
        # Also will not work if the vertex occurs at x = 0 so this will just give a straight line
        # in this case

        step_y = (turn_point[1] - entrance_loc[1])/num_points

        destinations = []
        for i in range(0, num_points):
            y = i*step_y + entrance_loc[1]
            destinations.append((entrance_loc[0], y))


    else:
        s_x, s_y = entrance_loc
        v_x, v_y = turn_point

        # Solving some quadratics
        b = (v_y - s_y) / ((((s_x**2)-(v_x**2))/(2*v_x))+v_x -s_x)
        a = -b/(2*v_x)
        c = v_y - a*(v_x**2) - b*v_x

        step_x = (break_point - s_x)/num_points
        destinations = []
        for i in range(0, num_points):
            x = i*step_x
            x += s_x
            y = a*(x**2)+(b*x)+c

            destinations.append((x, y))

    return destinations

def circle_trajectory(radius, center, start_theta, num_points, break_theta):

    theta_index = start_theta
    delta_theta = (break_theta-start_theta) / num_points
    trajectory = []
    while theta_index < break_theta:
        trajectory.append((radius * math.cos(theta_index) + center[0], radius*math.sin(theta_index) + center[1]))
        theta_index += delta_theta
    return trajectory