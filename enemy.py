import arcade
from weapon import Weapon
from bullet import Bullet
import math
import copy
import random

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .25


class Enemy(arcade.Sprite):
    """
    Extension of sprite class to represent some of the enemies used in the game
    :param filename: name of the .png file used for the sprite
    :param destination_list a list of (x,y) coordinates
    :param position_in_battle_line: when added to a battle line this is its relative position to the other enemies
    :param scale: the scaling of the .png file to fit the game
    :param hp: an integer representing how many shots it takes to destroy the enemy
    :param time_between_firing: time in seconds between when the enemy fires
    :param speed-to_formation: the speed of the enemy as it moves to its battle_line formation
    :param speed_in_formation: the speed at which the enemy travels while oscillating back and forth in a battle_line
    :param time_until_charge: how many seconds until the enemy leaves the battle_line position and charges the player
    :param despawn_timer: how much time in seconds it takes the enemy to despawn and remove itself from any sprite lists
    """
    def __init__(self,
                 filename,
                 destination_list,
                 position_in_battle_line=0,
                 scale=0.375,
                 weapon=Weapon(),
                 hp=1,
                 time_between_firing=2.0,
                 speed_to_formation=2,
                 speed_in_formation=2,
                 time_until_charge=10.0,
                 despawn_timer=500
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
        self.time_until_charge = time_until_charge
        self.lifetime = 0
        self.charge_destination = None
        self.firing_pattern = None
        self.firing_in_pattern = False
        self.despawn_timer = despawn_timer  # used to despawn enemies that have existed too long
        self.despawn = False

    def update(self, delta_time: float = 1 / 60):
        if self.center_y < 0:
            self.remove_from_sprite_lists()

        if self.move_state == 'initial':
            # Move to destination
            delta_x = self.destination[0] - self.center_x
            delta_y = self.destination[1] - self.center_y
            dist = math.sqrt(delta_x**2 + delta_y**2)

            if dist < 6:
                # print('Destination Achieved')
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

        elif self.move_state == 'charging':
            destination = self.charge_destination
            delta_x = destination[0] - self.center_x
            delta_y = destination[1] - self.center_y

            dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

            change_x = (delta_x * self.speed_to_formation) / dist
            change_y = (delta_y * self.speed_to_formation) / dist

            self.center_x += change_x
            self.center_y += change_y

        self.time_since_last_firing += delta_time
        self.lifetime += delta_time

        # Check if the enemy has fired recently
        if self.firing_in_pattern:
            # Check time since we last fired
            if self.time_since_last_firing >= self.firing_pattern.time_to_fire():
                # Reset firing timer
                self.time_since_last_firing = 0
                self.firing_pattern.next_fire()

                # Set need to fire as True
                self.to_fire = True

        else:
            # Check this value against time_between_firing
            if self.time_since_last_firing >= self.time_between_firing:

                # Reset firing timer
                self.time_since_last_firing = 0

                # Set need to fire as True
                self.to_fire = True

        # Check if it's time to charge
        if self.lifetime > self.time_until_charge:
            self.move_state = 'charging'

        # Check if the enemy is ready to despawn
        if self.lifetime > self.despawn_timer:
            # This will be handled in main
            self.despawn = True

    def fire(self):
        self.to_fire = False
        bullet = self.weapon.fire(self.center_x, self.top - self.height)
        return bullet

    def set_firing_pattern(self, firing_pattern):
        self.firing_pattern = firing_pattern
        self.firing_in_pattern = True


class Singleton(arcade.Sprite):
    """
    Singleton enemies are used when you want to specify exactly where an enemy path takes it
    without relying on any battle_lines.

    Always put the charging destination at a negative y value so that the sprite despawns

    :param similar to enemy parameters
    """
    def __init__(self,
                 filename,
                 destination_list,
                 scale=0.375,
                 weapon=Weapon(),
                 hp=1,
                 time_between_firing=2.0,
                 speed_to_formation=2,
                 despawn_timer=500,
                 charge_destination=(0, 0)
                 ):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.weapon = weapon
        self.weapon.friendly = False
        self.time_since_last_firing = 0
        self.time_between_firing = time_between_firing
        self.to_fire = False
        self.destination_list = destination_list
        self.speed_to_formation = speed_to_formation
        self.destination = self.destination_list[0]
        self.lifetime = 0
        self.move_state = 'initial'
        self.charge_destination = charge_destination
        self.firing_pattern = None
        self.firing_in_pattern = False
        self.despawn_timer = despawn_timer  # used to despawn enemies that have existed too long
        self.despawn = False

    def update(self, delta_time: float = 1 / 60):

        if self.move_state == 'initial':
            # Move to destination
            delta_x = self.destination[0] - self.center_x
            delta_y = self.destination[1] - self.center_y
            dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

            if dist < 6:
                # print('Destination Achieved')
                self.center_x = self.destination[0]
                self.center_y = self.destination[1]
                # Remove this destination from the list
                self.destination_list.pop(0)

                # last destination achieved
                if len(self.destination_list) < 2:
                    self.move_state = 'charging'

                self.destination = self.destination_list[0]

            else:
                change_x = (delta_x * self.speed_to_formation) / dist
                change_y = (delta_y * self.speed_to_formation) / dist

                self.center_x += change_x
                self.center_y += change_y

        elif self.move_state == 'charging':
            destination = self.charge_destination
            delta_x = destination[0] - self.center_x
            delta_y = destination[1] - self.center_y

            dist = math.sqrt(delta_x ** 2 + delta_y ** 2)

            change_x = (delta_x * self.speed_to_formation) / dist
            change_y = (delta_y * self.speed_to_formation) / dist

            self.center_x += change_x
            self.center_y += change_y

            if self.center_y < 0:
                self.remove_from_sprite_lists()

        # Check if the enemy is ready to despawn
        if self.lifetime > self.despawn_timer:
            # This will be handled in main
            self.despawn = True

        self.time_since_last_firing += delta_time
        self.lifetime += delta_time

        # Check if the enemy has fired recently
        if self.firing_in_pattern:
            # Check time since we last fired

            if self.time_since_last_firing >= self.firing_pattern.time_to_fire():
                # Reset firing timer
                self.time_since_last_firing = 0
                self.firing_pattern.next_fire()

                # Set need to fire as True
                self.to_fire = True

        else:
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

    def set_firing_pattern(self, firing_pattern):
        self.firing_pattern = firing_pattern
        self.firing_in_pattern = True


class Swarmer(arcade.Sprite):
    """
    A Swarmer is a toned down Enemy whose sole purpose is to move and not shoot,
    Should a swarmer find it's last destination it will despawn
    """
    def __init__(self,
                 filename,
                 destination_list,
                 scale=0.375,
                 hp=1,
                 speed_to_formation=2,
                 despawn_timer=500
                 ):
        super().__init__(filename=filename, scale=scale)
        self.hp = hp
        self.destination_list = destination_list
        self.speed_to_formation = speed_to_formation
        self.move_state = 'initial'
        self.destination = self.destination_list[0]
        self.lifetime = 0
        self.despawn_timer = despawn_timer  # used to despawn enemies that have existed too long
        self.despawn = False
        self.to_fire = False

    def update(self, delta_time: float = 1 / 60):
        if len(self.destination_list) < 2:
            self.remove_from_sprite_lists()

        if self.move_state == 'initial':
            # Move to destination
            delta_x = self.destination[0] - self.center_x
            delta_y = self.destination[1] - self.center_y
            dist = math.sqrt(delta_x**2 + delta_y**2)

            if dist < 6:
                # print('Destination Achieved')
                self.center_x = self.destination[0]
                self.center_y = self.destination[1]
                # Remove this destination from the list
                self.destination_list.pop(0)

                # last destination achieved
                if len(self.destination_list) < 2:
                    self.remove_from_sprite_lists()

                self.destination = self.destination_list[0]

            else:
                change_x = (delta_x * self.speed_to_formation) / dist
                change_y = (delta_y * self.speed_to_formation) / dist

                self.center_x += change_x
                self.center_y += change_y

        # Check if the enemy is ready to despawn
        if self.lifetime > self.despawn_timer:
            # This will be handled in main
            self.despawn = True


class FiringPattern:
    """
    A Firing Pattern is used by a Battle_Line to control when a formation can shoot
    It dictates whether the enemies are in open fire (fire according to their fire rate) or if they are
    to fire a specific pattern.
    :param timing_list a list of integers which dictates the delay between shots
    """
    def __init__(self, timing_list):
        self.timing_list = timing_list
        self.firing_index = 0

    def time_to_fire(self):

        return self.timing_list[self.firing_index]

    def next_fire(self):
        self.firing_index += 1

        if self.firing_index >= len(self.timing_list):
            self.firing_index = 0

    def set_position(self, index):
        self.firing_index = index


"""
ENEMY CREATION FUNCTIONS
"""


def create_random_level_one_bug(destination_list):

    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=10)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=10)
    enemy = Enemy(filename="Enemy_1.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  speed_to_formation=5,
                  destination_list=destination_list,
                  time_between_firing=(random.random() % 4) + 4,
                  time_until_charge=(random.random() % 20) + 10,)
    return copy.deepcopy(enemy)


def create_random_level_two_bug(destination_list):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=12)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=12)
    enemy = Enemy(filename="Enemy_2.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  hp=2,
                  speed_to_formation=4,
                  destination_list=destination_list,
                  time_between_firing=(random.random() % 4) + 3,
                  time_until_charge=(random.random() % 20) + 15
                  )
    return copy.deepcopy(enemy)


def create_random_level_three_bug(destination_list):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=14)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=14)
    enemy = Enemy(filename="Enemy_3.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  hp=3,
                  speed_to_formation=2,
                  time_between_firing=1.7,
                  destination_list=destination_list)
    return copy.deepcopy(enemy)

# Bug generators for 2nd Level


def create_L4_bug(destination_list, firing_pattern):
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=14)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=5)
    # ENEMY 4 Sprite needed#
    enemy = Enemy(filename="Enemy_3.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon,
                  hp=10,
                  speed_to_formation=1,
                  time_between_firing=0.1,
                  destination_list=destination_list)
    enemy.set_firing_pattern(firing_pattern)

    return copy.deepcopy(enemy)


def create_swarmer(destination_list):
    enemy = Swarmer(filename="Enemy_1.png",
                    destination_list=destination_list,
                    hp=1,
                    speed_to_formation=5,
                    scale=ENEMY_SPRITE_SCALING/2
                    )

    return copy.deepcopy(enemy)


def create_singleton(destination_list, charge_destination, firing_pattern):
    goo_shot = Bullet(filename="goo_shot_1.png", speed=14)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=5)
    enemy = Singleton(filename="Enemy_2.png",
                      scale=ENEMY_SPRITE_SCALING,
                      weapon=enemy_weapon,
                      hp=5,
                      speed_to_formation=1,
                      destination_list=destination_list,
                      charge_destination=charge_destination)
    enemy.set_firing_pattern(firing_pattern)

    return copy.deepcopy(enemy)
