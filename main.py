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
from enemy import Enemy, create_level_one_bug, create_level_two_bug, create_level_three_bug
from battle_line import Horizontal_Battle_Line
import random
import math
import arcade.gui
from arcade.experimental import Shadertoy

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
ENEMY_SPRITE_SCALING = .0375
PLAYER_SPRITE_SCALING = .5
SCREEN_TITLE = "Galaga"

# class Level_One:
#     def __init__(self):
#         battle_line_1 = Horizontal_Battle_Line()
#         battle_line_2 = Horizontal_Battle_Line()
#         battle_line_3 = Horizontal_Battle_Line()
#         battle_line_4 = Horizontal_Battle_Line()
#         battle_line_5 = Horizontal_Battle_Line()


class Star:
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset_pos(self):
        # Reset flake to random position above screen
        self.y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 100)
        self.x = random.randrange(SCREEN_WIDTH)

class StartButton(arcade.gui.UIFlatButton):
    """
    StartButton class for start screen
    """
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        game_view = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
        game_view.setup()
        game_view.window.show_view(game_view)

"""
class EndButton(arcade.gui.UIFlatButton):

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        game_view = EndScreen(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
        game_view.setup()
        game_view.window.show_view(game_view)
"""
class StartScreen(arcade.View):

    def setup(self):
        self.logo = arcade.Sprite("Galaga.png", .15)
        self.logo.center_x = SCREEN_WIDTH/2
        self.logo.center_y = SCREEN_HEIGHT - 200
    def on_show_view(self):
        # SET UP START SCREEN

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.start_screen_alignment = arcade.gui.UIBoxLayout(space_between=20)

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": arcade.color.WHITE,
            "border_width": 5,
            "border_color": None,
            "bg_color": (43, 80, 227),
            "bg_color_pressed": (173, 27, 10),
            "bg_color_hover": (43, 80, 227),
            "border_color_hover": (173, 27, 10),
            "border_color_pressed": (173, 27, 10)
        }

        start_button_1 = StartButton(text="One Player", width=150, style=default_style)
        self.start_screen_alignment.add(start_button_1)
        #start_button_2 = StartButton(text="Two Players", width=150, style=default_style)
        #self.start_screen_alignment.add(start_button_2)
        end_button = EndButton(text="end screen", width=150, style=default_style)
        self.start_screen_alignment.add(end_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.start_screen_alignment)
        )


    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.logo.draw()

class MyGame(arcade.View):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__()

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

        self.enemy_list = Horizontal_Battle_Line(speed=1, num_ships=10, left_pos=100, right_pos=400, depth=600)
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
        enemy_1.center_y = 750
        enemy_1.angle = 180
        self.enemy_list.add_enemy(0, enemy_1)

        enemy_2 = create_level_one_bug()
        enemy_2.center_x = 500
        enemy_2.center_y = 750
        enemy_2.angle = 180
        self.enemy_list.add_enemy(1, enemy_2)

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

        #GAME PLAY DISPLAY

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
            hits = arcade.check_for_collision_with_list(bullet, self.player_list)

            if len(hits) > 0:
                bullet.remove_from_sprite_lists()

                # Player hurt and loses a life



            # Bullet is off the below screen
            if bullet.bottom < 0:
                bullet.remove_from_sprite_lists()


        for bullet in self.player_bullet_list:
            # Bullet contact with enemy sprite
            hits = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if len(hits) > 0:
                bullet.remove_from_sprite_lists()
                for enemy_hit in hits:
                    enemy_hit.hp -= bullet.damage
                    if enemy_hit.hp <= 0:
                        enemy_hit.remove_from_sprite_lists()
                        # Explosion here

            # Bullet is above the screen
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

class ReturnStartButton(arcade.gui.UIFlatButton):
    """ Return to start screen"""

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        start_view = StartScreen()
        start_view.setup()
        start_view.window.show_view(start_view)

class EndScreen(arcade.View):

    def setup(self):
        self.logo = arcade.Sprite("Galaga.png", .15)
        self.logo.center_x = SCREEN_WIDTH/2
        self.logo.center_y = SCREEN_HEIGHT - 200

    def on_show_view(self):
        # sets up the end screen

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.end_screen_alignment = arcade.gui.UIBoxLayout(space_between=20)

        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "font_color_pressed": arcade.color.WHITE,
            "border_width": 5,
            "border_color": None,
            "bg_color": (43, 80, 227),
            "bg_color_pressed": (173, 27, 10),
            "bg_color_hover": (43, 80, 227),
            "border_color_hover": (173, 27, 10),
            "border_color_pressed": (173, 27, 10)
        }

        return_button = ReturnStartButton(text="Return to Start", width=150, style=default_style)
        self.end_screen_alignment.add(return_button)
        replay_button = StartButton(text="Play Again", width=150, style=default_style)
        self.end_screen_alignment.add(replay_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.end_screen_alignment)
        )

    def on_draw(self):
        self.clear()
        self.manager.draw()
        # draws GAME OVER text
        start_x = 0
        start_y = (SCREEN_HEIGHT / 2) + 50
        arcade.draw_text("GAME OVER", start_x, start_y, arcade.color.LIGHT_BLUE, 20, width=SCREEN_WIDTH, align="center")

        start_x -= 50
        start_y = (SCREEN_HEIGHT / 2) + 30
        arcade.draw_text("SCORE:", start_x, start_y, arcade.color.WHITE, 10, width=SCREEN_WIDTH, align="center")
        self.logo.draw()

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Galaga")
    start_view = StartScreen()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

