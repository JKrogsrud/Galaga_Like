"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
from weapon import Weapon
from bullet import Bullet
from player import Player
from enemy import Enemy
import random
import math
import copy
from arcade.experimental import Shadertoy

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .5
SCREEN_TITLE = "Galaga"


def create_level_one_bug():
    goo_shot = Bullet(filename="goo_shot_1.png",
                      speed=10)
    enemy_weapon = Weapon(friendly=False, requires_ammo=False, bullet_type=goo_shot, bullet_speed=10)
    enemy = Enemy(filename="Enemy_1.png",
                  scale=ENEMY_SPRITE_SCALING,
                  weapon=enemy_weapon)
    return copy.deepcopy(enemy)

class Star:
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        # Reset flake to random position above screen
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.enemy_list = None
        self.enemy_bullet_list = None
        self.player_list = None
        self.player_bullet_list = None
        self.background_list = None

        # Loads a file and creates a shader from it
        #window_size = self.get_size()
        #self.shadertoy = Shadertoy.create_from_file(window_size, "Purple.glsl")


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Setup Background
        self.background_list = []

        for i in range(50):
            star = Star()

            # Randomly position it
            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT)

            # Setup other variables
            star.size = random.randrange(4)
            star.speed = random.randrange(20, 40)
            star.angle = random.uniform(math.pi, math.pi * 2)

            self.background_list.append(star)

        arcade.set_background_color(arcade.color.BLACK)
        # Create your sprites and sprite lists here

        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # if level == 1 or level == 2:
        #     num_of_enemies_1 = 6
        # elif level == 3 or level == 4:
        #     num_of_enemies_1 = 10
        # else:
        #     num_of_enemies_1 = 12
        #
        # for i in range(NUM_OF_ENEMY_1):
        #     self.enemy_sprite = Enemy("Enemy_1.png", scale=ENEMY_SPRITE_SCALING)
        #     if NUM_OF_ENEMY_1 <= 6:
        #
        #         self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH-150)/NUM_OF_ENEMY_1)*i
        #         self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
        #     else:
        #         if i <= 6:
        #             spacing = (SCREEN_WIDTH-150)
        #             self.enemy_sprite.center_x = 75 + (SCREEN_WIDTH-150)/7/2 + ((SCREEN_WIDTH - 150)/7)*(i)
        #             self.enemy_sprite.center_y = SCREEN_HEIGHT - 200
        #         else:
        #             self.enemy_sprite.center_x = 75+ (SCREEN_WIDTH-150)/(NUM_OF_ENEMY_1- 7)/2 + ((SCREEN_WIDTH - 150)/(NUM_OF_ENEMY_1- 7))*(i - 7)
        #             self.enemy_sprite.center_y = SCREEN_HEIGHT - 150
        #
        #     self.enemy_list.append(self.enemy_sprite)
        #
        # # Set up the enemies for list 2
        # for i in range(NUM_OF_ENEMY_2):
        #     self.enemy_sprite = Enemy("Enemy_2.png", ENEMY_SPRITE_SCALING)
        #     self.enemy_sprite.center_x = 75 + + (SCREEN_WIDTH - 150) / NUM_OF_ENEMY_2 / 2 + (
        #                 (SCREEN_WIDTH - 150) / NUM_OF_ENEMY_2) * i
        #     self.enemy_sprite.center_y = SCREEN_HEIGHT - 100
        #     self.enemy_list.append(self.enemy_sprite)
        #
        # # Set up the enemies for list 3
        # for i in range(NUM_OF_ENEMY_3):
        #     self.enemy_sprite = Enemy("Enemy_3.png", ENEMY_SPRITE_SCALING)
        #     self.enemy_sprite.center_x = 75 + + (SCREEN_WIDTH-150)/NUM_OF_ENEMY_3/2 + ((SCREEN_WIDTH-150)/NUM_OF_ENEMY_3)*i
        #     self.enemy_sprite.center_y = SCREEN_HEIGHT - 50
        #     self.enemy_list.append(self.enemy_sprite)

        # Setup enemy sprites
        enemy_1 = create_level_one_bug()
        enemy_1.center_x = 40
        enemy_1.center_y = 500
        enemy_1.angle = math.radians(math.pi)
        self.enemy_list.append(enemy_1)

        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = int(SCREEN_WIDTH / 2)
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        # Setup Background
        self.background_list = []

        for i in range(50):
            star = Star()

            # Randomly position it
            star.x = random.randrange(SCREEN_WIDTH)
            star.y = random.randrange(SCREEN_HEIGHT)

            # Setup other variables
            star.size = random.randrange(4)
            star.speed = random.randrange(20, 40)
            star.angle = random.uniform(math.pi, math.pi * 2)

            self.background_list.append(star)

        arcade.set_background_color(arcade.color.BLACK)

        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.

        self.clear()

        for star in self.background_list:
            arcade.draw_circle_filled(star.x, star.y, star.size, arcade.color.YELLOW_ORANGE)

        # Call draw() on all your sprite lists below
        self.enemy_list.draw()
        self.enemy_bullet_list.draw()
        self.player_list.draw()
        self.player_bullet_list.draw()

        # Run the GLSL code
        #self.shadertoy.render()
        #self.shadertoy.render()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Animate all the stars falling
        for star in self.background_list:
            star.y -= star.speed * delta_time

            # Check if star has fallen below screen
            if star.y < 0:
                star.reset_pos()


        # Call update on bullet sprites
        self.enemy_bullet_list.update()
        self.player_bullet_list.update()
        self.player_list.update()

        # Check stuff
        for bullet in self.enemy_bullet_list:
            # Bullet contact with player sprite

            # Bullet is off the below screen
            if bullet.bottom < 0:
                bullet.remove_from_sprite_lists()

        for bullet in self.player_bullet_list:
            # Bullet contact with enemy sprite
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        # Move Enemy Ships
        self.enemy_list.update()

        # Check if any enemies are ready to fire
        for enemy in self.enemy_list:
            if enemy.to_fire:
                bullet = enemy.fire()
                self.enemy_bullet_list.append(bullet)
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == 32:
            # Fire a weapon from current weapon of player at their location
            bullet = self.player_sprite.fire()
            self.player_bullet_list.append(bullet)
        elif key == arcade.key.LEFT:
            self.player_sprite.left_pressed = True
            self.player_sprite.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.player_sprite.right_pressed = True
            self.player_sprite.update_player_speed()

        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.LEFT:
            self.player_sprite.left_pressed = False
            self.player_sprite.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.player_sprite.right_pressed = False
            self.player_sprite.update_player_speed()
        pass


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()