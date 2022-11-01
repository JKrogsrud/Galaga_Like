import arcade
from weapon import Weapon
from bullet import Bullet
import math
import copy
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .5


class Enemy(arcade.Sprite):
    def __init__(self,
                 filename,
                 destination_list,
                 position_in_battle_line=0,
                 scale=0.375,
                 weapon=Weapon(),
                 hp=1,
                 time_between_firing=2.0,
                 speed_to_formation=2,
                 speed_in_formation=2
                 ):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.weapon = weapon
        self.weapon.friendly = False
        self.time_since_last_firing = 0
        self.time_between_firing = time_between_firing
        self.to_fire = False
        self.destination_list = destination_list
        self.position_in_battle_line = position_in_battle_line
        self.speed_to_formation = speed_to_formation
        self.speed_in_formation = speed_in_formation
        self.move_state = 'initial'
        self.destination = self.destination_list[0]

    def update(self, delta_time: float = 1 / 60):
        if self.move_state == 'initial':
            # Move to destination
            delta_x = self.destination[0] - self.center_x
            delta_y = self.destination[1] - self.center_y
            dist = math.sqrt(delta_x**2 + delta_y**2)

            if dist < 6:
                #print('Destination Achieved')
                self.center_x = self.destination[0]
                self.center_y = self.destination[1]
                # Remove this destination from the list
                self.destination_list.pop(0)

                self.destination = self.destination_list[0]

                # last destination achieved
                if len(self.destination_list) == 0:
                    self.move_state = 'to_battle_pos'
            else:
                change_x = (delta_x * self.speed_to_formation) / dist
                change_y = (delta_y * self.speed_to_formation) / dist

                self.center_x += change_x
                self.center_y += change_y
        elif self.move_state == 'to_battle_pos':
            # Move to destination
            destination = self.destination_list[0]
            delta_x = destination[0] - self.center_x
            delta_y = destination[1] - self.center_y
            dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

            if dist < 5:
                self.center_x = destination[0]
                self.center_y = destination[1]
                self.move_state = 'in_formation'

            else:
                change_x = (delta_x * self.speed_to_formation) / dist
                change_y = (delta_y * self.speed_to_formation) / dist

                self.center_x += change_x
                self.center_y += change_y
        elif self.move_state == 'in_formation':
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


def create_level_one_bug(destination_list):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=10)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=10)
    enemy = Enemy(filename="Enemy_1.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  speed_to_formation=5,
                  destination_list=destination_list,
                  time_between_firing= (random.random() % 4)+2)
    return copy.deepcopy(enemy)


def create_level_two_bug(destination_list):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=12)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=12)
    enemy = Enemy(filename="Enemy_2.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  hp=2,
                  speed_to_formation=4,
                  time_between_firing=1.5,
                  destination_list=destination_list)
    return copy.deepcopy(enemy)

def create_level_three_bug(destination_list):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=14)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=14)
    enemy = Enemy(filename="Enemy_3.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  hp=3,
                  speed_to_formation=2,
                  time_between_firing=1.3,
                  destination_list=destination_list)
    return copy.deepcopy(enemy)
